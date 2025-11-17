import tempfile
from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
import torch
from tqdm.auto import tqdm
from transformers.modeling_outputs import BaseModelOutputWithPoolingAndCrossAttentions

from selfclean.cleaner.issue_manager import IssueTypes
from selfclean.core.src.utils.utils import get_device

ARR_TYPE = Union[np.ndarray, np.memmap, torch.Tensor]


def embed_dataset(
    torch_dataset: torch.utils.data.DataLoader,
    model: Optional[torch.nn.Sequential],
    n_layers: int,
    normalize: bool = False,
    memmap: bool = True,
    memmap_path: Union[Path, str, None] = None,
    return_only_embedding_and_labels: bool = False,
    tqdm_desc: Optional[str] = None,
) -> Union[Tuple[ARR_TYPE, ARR_TYPE, ARR_TYPE, ARR_TYPE], Tuple[ARR_TYPE, ARR_TYPE]]:
    labels = []
    paths = []
    batch_size = torch_dataset.batch_size
    iterator = tqdm(
        enumerate(torch_dataset),
        position=0,
        leave=True,
        total=len(torch_dataset),
        desc=tqdm_desc,
    )
    # calculate the embedding dimension for memmap array
    _batch = torch_dataset.dataset[0][0][None, ...]
    if model is not None:
        _batch = _batch.to(model.device)
    batch_dim = tuple(_batch.shape)[1:]
    if (
        type(model) is torch.jit._script.RecursiveScriptModule
        or type(model) is torch.nn.Sequential
    ):
        emb_dim = model(_batch).squeeze().shape[0]
    elif model is None:
        emb_dim = _batch.squeeze().shape[0]
    else:
        emb_dim = model(_batch, n_layers=n_layers).squeeze().shape[0]
    # create the memmap's
    if memmap:
        memmap_path = create_memmap_path(memmap_path=memmap_path)
        emb_space = create_memmap(
            memmap_path,
            "embedding_space.dat",
            len(torch_dataset.dataset),
            *(emb_dim,),
        )
        if not return_only_embedding_and_labels:
            images = create_memmap(
                memmap_path,
                "images.dat",
                len(torch_dataset.dataset),
                *batch_dim,
            )
    else:
        emb_space = np.zeros(shape=(len(torch_dataset.dataset), emb_dim))
        if not return_only_embedding_and_labels:
            images = np.zeros(shape=(len(torch_dataset.dataset), *batch_dim))
    del emb_dim, batch_dim, _batch
    # embed the dataset
    for i, batch_tup in iterator:
        if len(batch_tup) == 3:
            batch, path, label = batch_tup
        elif len(batch_tup) == 2:
            batch, label = batch_tup
            path = None
        else:
            raise ValueError("Unknown batch tuple.")

        with torch.no_grad():
            if model is not None:
                batch = batch.to(model.device)
            if (
                type(model) is torch.jit._script.RecursiveScriptModule
                or type(model) is torch.nn.Sequential
            ):
                emb = model(batch)
            elif model is None:
                emb = batch
            else:
                emb = model(batch, n_layers=n_layers)
            emb = emb.squeeze()
            if normalize:
                emb = torch.nn.functional.normalize(emb, dim=-1, p=2)
            emb_space[batch_size * i : batch_size * (i + 1), :] = emb.cpu()
            if type(emb_space) is np.memmap:
                emb_space.flush()
            labels.append(label.cpu())
            if not return_only_embedding_and_labels:
                images[batch_size * i : batch_size * (i + 1), :] = batch.cpu()
                if type(images) is np.memmap:
                    images.flush()
                if path is not None:
                    paths += path
    labels = torch.concat(labels).cpu()
    if return_only_embedding_and_labels:
        return emb_space, labels
    if len(paths) > 0:
        paths = np.array(paths)
    else:
        paths = None
    return emb_space, labels, images, paths

def embed_text_dataset(torch_dataset, model, batch_size, normalize=True, tqdm_desc="", issues_to_detect=[]):
    """Embed a text dataset using the given model."""
    from tqdm.auto import tqdm

    model.eval()
    embeddings = []
    context_only_embeddings = []
    labels = []
    paths = []
    categories = []

    with torch.no_grad():
        for batch in tqdm(torch_dataset, desc=tqdm_desc):
            # Unpack batch (inputs, label)
            inputs, label, category, _, context_only_inputs, context_only_flag, *_ = batch
            inputs = {k: v.to(get_device()) for k, v in inputs.items()}

            # Get embeddings
            emb = model(**inputs)

            if isinstance(emb, BaseModelOutputWithPoolingAndCrossAttentions):
                emb = emb.pooler_output

            if normalize:
                emb = torch.nn.functional.normalize(emb, p=2, dim=1)

            [embeddings.append(emb[i].cpu().numpy()) for i in range(emb.shape[0])]

            if IssueTypes.NEAR_DUPLICATES_Q in issues_to_detect:
                # Also embed context only
                filtered_context_only_inputs = {'input_ids': torch.tensor([], dtype=torch.int64),
                                                'attention_mask': torch.tensor([], dtype=torch.int64)}
                for i in range(min(batch_size, len(label))):
                    flag_ = context_only_flag[i]
                    if flag_:
                        for k in context_only_inputs.keys():
                            filtered_context_only_inputs[k] = torch.cat(
                                (filtered_context_only_inputs[k], context_only_inputs[k][i].unsqueeze(0)), dim=0
                            )

                filtered_context_only_inputs = {k: v.to(get_device()) for k, v in filtered_context_only_inputs.items()}
                context_emb = model(**filtered_context_only_inputs)
                if isinstance(context_emb, BaseModelOutputWithPoolingAndCrossAttentions):
                    context_emb = context_emb.pooler_output
                if normalize:
                    context_emb = torch.nn.functional.normalize(context_emb, p=2, dim=1)
                [context_only_embeddings.append(context_emb[i].cpu().numpy()) for i in range(context_emb.shape[0])]

            labels.extend(label.cpu().numpy())
            categories.extend(category)

            # Use task_id as path identifier
            task_ids = [f"task_{i}" for i in range(len(paths), len(paths) + len(label))]
            paths.extend(task_ids)

    return embeddings, labels, paths, categories, context_only_embeddings


def create_memmap(memmap_path: Path, memmap_file_name: str, len_dataset: int, *dims):
    memmap_file = memmap_path / memmap_file_name
    if memmap_file.exists():
        memmap_file.unlink()
    memmap = np.memmap(
        str(memmap_file),
        dtype=np.float32,
        mode="w+",
        shape=(len_dataset, *dims),
    )
    return memmap


def create_memmap_path(memmap_path: Union[str, Path, None]) -> Path:
    if memmap_path is None:
        # temporary folder for saving memory map
        memmap_path = Path(tempfile.mkdtemp())
    else:
        # make sure the path exists
        memmap_path = Path(memmap_path)
        memmap_path.mkdir(parents=True, exist_ok=True)
    return memmap_path

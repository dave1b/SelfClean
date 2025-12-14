import random

# Redefine the categories
categories = {
    "Programming Snippets": [
        "Python", "JavaScript", "Java", "C++", "SQL", "Bash", "HTML", "CSS", "Rust", "Go"
    ],
    "Non-readable/Gibberish": [
        "Random characters", "Unicode/Emoji mix", "Keyboard smashes",
        "Base64 encoded", "URL-encoded", "Hex dump", "Binary data",
        "OCR errors", "Voice transcription errors", "Mixed symbols"
    ],
    "Bytecode/Compiled Output": [
        "Python bytecode", "Java bytecode", "Assembly",
        "LLVM IR", "WebAssembly", "JVM bytecode",
        ".NET IL", "Machine code", "Disassembly", "Obfuscated code"
    ],
    "Mathematical/Scientific Notation": [
        "Equations", "LaTeX", "Chemical formulas",
        "Physics formulas", "Statistical notation",
        "Algebraic expressions", "Calculus", "Logic",
        "Set theory", "Matrix notation"
    ],
    "Data Serialization Formats": [
        "JSON", "XML", "YAML", "CSV", "TOML",
        "INI", "Protocol Buffers", "MessagePack",
        "Avro", "BSON"
    ],
    "Network/Protocol Data": [
        "HTTP headers", "TCP/IP packets", "DNS records",
        "Email headers", "WebSocket frames", "FTP commands",
        "SSH logs", "TLS handshake", "REST API responses", "GraphQL queries"
    ],
    "Natural Language (Non-English)": [
        "Spanish", "French", "German", "Chinese",
        "Japanese", "Arabic", "Russian", "Hindi",
        "Portuguese", "Italian"
    ],
    "Log/Error Messages": [
        "Stack traces", "System logs", "Application logs",
        "Security logs", "Database logs", "Web server logs",
        "Kernel logs", "Crash dumps", "Audit logs", "Debug output"
    ],
    "Placeholder/Lorem Ipsum": [
        "Lorem Ipsum", "Fake names", "Fake addresses",
        "Fake phone numbers", "Fake emails", "Fake company names",
        "Fake product descriptions", "Fake reviews",
        "Fake social media posts"
    ],
    "Mixed/Edge Cases": [
        "Code + comments", "Markdown", "Template strings",
        "Environment variables", "Configuration files",
        "Dockerfiles", "Makefiles", "Git diffs",
        "Code documentation", "Inline HTML"
    ],
    "Shell Scripting": [
        "Bash scripts", "PowerShell scripts", "Batch scripts",
        "Shell one-liners", "Cron jobs", "Awk scripts",
        "Sed commands", "Grepping logs", "Piping commands", "Redirecting output"
    ],
    "Config Files": [
        "JSON config", "YAML config", "INI config",
        "TOML config", "XML config", "Properties files",
        "Environment files", "Nginx config", "Apache config", "Docker Compose"
    ],
    "Spam/Advertisement Text": [
        "Email spam", "SMS spam", "Pop-up ads",
        "Phishing messages", "Scam offers", "Fake promotions",
        "Clickbait", "Malware warnings", "Chain letters", "Survey scams"
    ],
    "ASCII Art": [
        "Simple art", "Complex art", "Text-based games",
        "Banners", "Emoticon art", "Diagrams",
        "Tables", "Flowcharts", "Memes", "Text-based UI"
    ]
}

# --- EXPANDED AND FIXED TEMPLATES (All 140 subcategories covered) ---
simplified_example_templates = {
    # --- Programming Snippets (10) ---
    "Python": [
        "print('Hello, World!')",
        "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
        "x = [i**2 for i in range(10)]",
        "import math; print(math.pi)",
        "try: x = 1/0; except ZeroDivisionError: print('Error')"
    ],
    "JavaScript": [
        "console.log('Hello');",
        "const add = (a, b) => a + b;",
        "let arr = [1, 2, 3]; arr.map(x => x*2);",
        "fetch('/api/data').then(res => res.json());",
        "for (let i = 0; i < 5; i++) { console.log(i); }"
    ],
    "Java": [
        "public class Main { public static void main(String[] args) { System.out.println(\"Hello\"); } }",
        "int sum(int a, int b) { return a + b; }",
        "List<String> list = new ArrayList<>(); list.add(\"item\");",
        "try { throw new Exception(); } catch (Exception e) {}",
        "class MyRunnable implements Runnable { public void run() {} }"
    ],
    "C++": [
        "#include <iostream>; int main() { std::cout << \"Hello\" << std::endl; return 0; }",
        "int fib(int n) { return (n <= 1) ? n : fib(n-1) + fib(n-2); }",
        "std::vector<int> v = {1, 2, 3};",
        "class Car { public: void drive() {}; };",
        "try { throw 10; } catch (int e) { std::cout << e; }"
    ],
    "SQL": [
        "SELECT name, email FROM users WHERE id = 1;",
        "INSERT INTO products (name, price) VALUES ('Laptop', 1200.00);",
        "UPDATE orders SET status = 'shipped' WHERE id = 5;",
        "DELETE FROM logs WHERE timestamp < '2023-01-01';",
        "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(255));"
    ],
    "Bash": [
        "echo 'Hello, World!'",
        "grep -r error /var/log/ || echo 'No errors found'",
        "if [ -f file.txt ]; then cat file.txt; fi",
        "ps aux | grep python",
        "tar -czvf archive.tar.gz /path/to/dir"
    ],
    "HTML": [
        "<!DOCTYPE html><html><body><h1>Title</h1><p>Text.</p></body></html>",
        "<a href=\"/link\">Click Me</a>",
        "<img src=\"image.jpg\" alt=\"A photo\">",
        "<form><input type=\"text\" name=\"user\"></form>",
        "<ul><li>Item 1</li><li>Item 2</li></ul>"
    ],
    "CSS": [
        "body { font-family: Arial; background-color: #f0f0f0; }",
        ".container { width: 80%; margin: 0 auto; }",
        "#header { color: blue; padding: 10px; }",
        "@media (max-width: 600px) { body { font-size: 12px; } }",
        "a:hover { text-decoration: underline; }"
    ],
    "Rust": [
        "fn main() { println!(\"Hello\"); }",
        "let x: i32 = 5;",
        "let mut vec = Vec::new(); vec.push(1);",
        "struct Point { x: i32, y: i32 }",
        "match result { Ok(v) => v, Err(e) => panic!(\"Error: {}\", e) }"
    ],
    "Go": [
        "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Hello\") }",
        "var i int = 10",
        "if x > 5 { return true }",
        "type User struct { Name string }",
        "go func() { fmt.Println(\"Goroutine\") }()"
    ],

    # --- Non-readable/Gibberish (10) ---
    "Random characters": [
        "asdfjkl;qwer!@#$%^&*()_+",
        "zxcvbnm,./!@#$%^&*()_+",
        "1234567890!@#$%^&*()",
        "!@#$%^&*()_+qwertyuiop",
        "poiuytrewq!@#$%^&*()",
    ],
    "Unicode/Emoji mix": [
        "🚀🌕💻🔥📱🎮🌍🌟💡🔑",
        "😀😃😄😁😆😅😂🤣😊😇",
        "🌈🌟🌠🌦️🌧️☔️⛈️🌩️",
        "🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭",
        "🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮"
    ],
    "Keyboard smashes": [
        "gjhgjhkjghkjhghjlkjhlk",
        "qweqweasdzxccxzxcvasd",
        "!!!!!!!!!???????????",
        "................!!!!",
        "zxcmnbjhvcfgdfgcvb"
    ],
    "Base64 encoded": [
        "SGVsbG8gV29ybGQ=",
        "QWJjMTIzIT8k",
        "VGhpcyBpcyBhIHRlc3Q=",
        "ZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9S",
        "RGFzayBpcyBvZnRlbiB1c2Vk"
    ],
    "URL-encoded": [
        "key%3Dvalue%26param%3D1",
        "Hello%2C%20World%21",
        "file%2Fpath%2Fto%2Fresource",
        "%C3%A9cole%20%C3%A0%20Paris",
        "search%3Dquery%26limit%3D10"
    ],
    "Hex dump": [
        "0000 7a 78 63 76 62 6e 6d 20 31 32 33 0a",
        "48 65 6c 6c 6f 20 57 6f 72 6c 64 21",
        "0a 0d 0a 0d 0a 0d 0a 0d 0a 0d",
        "f0 9f 9a 80 e2 9c a8 61 73 64 66",
        "c3 a9 c3 a8 c3 a0 c3 b9 c3 b2"
    ],
    "Binary data": [
        "01001000 01100101 01101100 01101100 01101111",
        "10101010 01010101 11110000 00001111",
        "00000001 00000010 00000011 00000100",
        "11111111 11111111 00000000 00000000",
        "01101110 01100001 01101110 01101110 01100001"
    ],
    "OCR errors": [
        "The quick br0wn fox 1umps over the lazy d0g.",
        "A l\ybrary ls a great pl.ce to sludy.",
        "She sa\d \"l will be laeete.\" ",
        "d0cument v-1.0",
        "This is a tess t"
    ],
    "Voice transcription errors": [
        "I'm going to the store for a pair of socks and some serial.",
        "The whether today is going to be partly cloudy.",
        "He said he wood like to come with us.",
        "What is the cap little of France?",
        "Please meat me at the corner of the street."
    ],
    "Mixed symbols": [
        "##@!$%.^&**()_+-={}|[]\\<>?//",
        "~~~`|!@#$%^&*()_+",
        "&^%#@!.>~",
        "[1+2]*3/(4-5)",
        "<>[]{}()|\\"
    ],

    # --- Bytecode/Compiled Output (10) ---
    "Python bytecode": [
        "2 0 LOAD_GLOBAL              0 (print)\n  2 LOAD_CONST               1 (None)",
        "4 LOAD_FAST                0 (n)\n  6 LOAD_CONST               2 (1)",
        "8 COMPARE_OP               1 (<=)\n 10 POP_JUMP_IF_FALSE       20",
        "12 LOAD_CONST               2 (1)\n 14 RETURN_VALUE",
        "20 LOAD_GLOBAL              1 (factorial)\n 22 LOAD_FAST                0 (n)"
    ],
    "Java bytecode": [
        "0: aload_0\n 1: invokespecial #1 // Method java/lang/Object.\"<init>\":()V",
        "4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream;",
        "7: ldc #3 // String Hello\n 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V",
        "12: return",
        "iconst_0\nistore_1"
    ],
    "Assembly": [
        "MOV EAX, 1",
        "JMP LABEL_LOOP",
        "PUSH EBP",
        "CALL _printf",
        "RET"
    ],
    "LLVM IR": [
        "define i32 @main() #0 {\n  ret i32 0\n}",
        "%1 = alloca i32, align 4",
        "store i32 5, i32* %1, align 4",
        "call void @print_int(i32 %1)",
        "br label %loop_cond"
    ],
    "WebAssembly": [
        "(module\n  (func (export \"add\") (param $a i32) (param $b i32) (result i32)\n    local.get $a\n    local.get $b\n    i32.add))",
        "i32.const 42",
        "local.set $result",
        "call $print",
        "loop $L0"
    ],
    "JVM bytecode": [
        "aload_0",
        "invokevirtual java/lang/Object.getClass",
        "ldc \"Hello\"",
        "astore_1",
        "iload_1\n iconst_1\n iadd"
    ],
    ".NET IL": [
        "IL_0000: ldstr \"Hello World\"",
        "IL_0005: call void [mscorlib]System.Console::WriteLine(string)",
        "IL_000a: nop",
        "IL_000b: ret",
        "IL_0010: ldloc.0"
    ],
    "Machine code": [
        "55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8",
        "B8 01 00 00 00 C3",
        "E8 00 00 00 00 5D C3",
        "89 E5 83 C4 08 C9 C3",
        "48 83 C4 08 C3"
    ],
    "Disassembly": [
        "0x401000 <main+0>: push   %rbp",
        "0x401001 <main+1>: mov    %rsp,%rbp",
        "0x401004 <main+4>: sub    $0x10,%rsp",
        "0x401008 <main+8>: movl   $0x0,-0x4(%rbp)",
        "0x40100f <main+15>: callq  0x400000 <_start>"
    ],
    "Obfuscated code": [
        "eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};...",
        "var _0x4e21=['test','123','join','split']; (function(_0x5c4115,_0x4e2124){...",
        "const _0x1a8b = ['\x63\x6f\x6e\x73\x6f\x6c\x65', '\x6c\x6f\x67', '\x48\x65\x6c\x6c\x6f'];",
        "function a(b){return b-1}",
        "var x=0x10; while(x>0){x--}"
    ],

    # --- Mathematical/Scientific Notation (10) ---
    "Equations": [
        "E = mc^2",
        "a^2 + b^2 = c^2",
        "F = ma",
        "P V = n R T",
        "y = mx + b"
    ],
    "LaTeX": [
        "$\\int_0^1 x^2 dx$",
        "$$\\frac{d}{dx} e^x = e^x$$",
        "$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$",
        "$\\alpha \\beta \\gamma \\delta$",
        "$\\mathbf{A} \\vec{x} = \\vec{b}$"
    ],
    "Chemical formulas": [
        "H2O",
        "C6H12O6",
        "NaCl",
        "H2SO4",
        "CO2"
    ],
    "Physics formulas": [
        "$\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force)",
        "$\lambda = h / p$ (de Broglie wavelength)",
        "$\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty)",
        "$T = 2\pi\sqrt{L/g}$ (Pendulum period)",
        "$V = IR$ (Ohm's law)"
    ],
    "Statistical notation": [
        "$P(A|B) = \\frac{P(B|A)P(A)}{P(B)}$ (Bayes' theorem)",
        "$\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$",
        "$Z = (X - \mu) / \sigma$",
        "$H_0: \mu = 0$ (Null hypothesis)",
        "$R^2 = 1 - (SS_{res} / SS_{tot})$"
    ],
    "Algebraic expressions": [
        "$(x+y)^2 = x^2 + 2xy + y^2$",
        "$\frac{x}{2} + 5 = 10$",
        "$3x^2 - 4x + 1$",
        "$(a^2 - b^2) / (a - b) = a + b$",
        "$2(z + 3) - 7 = 9$"
    ],
    "Calculus": [
        "$\lim_{x \\to 0} \\frac{\sin x}{x} = 1$",
        "$\int x^n dx = \\frac{x^{n+1}}{n+1} + C$",
        "$\frac{\partial f}{\partial x}$",
        "$\nabla^2 V = 0$ (Laplace's equation)",
        "$\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$"
    ],
    "Logic": [
        "P $\\rightarrow$ Q",
        "$\\neg (A \land B) \equiv \neg A \lor \neg B$",
        "$\forall x (P(x) \rightarrow Q(x))$",
        "$(P \lor \neg P) \equiv \top$ (Law of excluded middle)",
        "$(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$"
    ],
    "Set theory": [
        "$A \cup B$",
        "$x \in \mathbb{R}$",
        "$A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$",
        "$\mathcal{P}(S)$ (Power set)",
        "$|S| = n$"
    ],
    "Matrix notation": [
        "$$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$",
        "$\mathbf{A} \mathbf{x} = \mathbf{b}$",
        "$\det(\mathbf{A})$",
        "$\mathbf{I}$ (Identity matrix)",
        "$\mathbf{A}^T$"
    ],

    # --- Data Serialization Formats (10) ---
    "JSON": [
        '{"key": "value", "array": [1, 2, 3]}',
        '{"name": "John", "age": 30, "city": "New York"}',
        '{"status": "success", "data": {"id": 123}}',
        '{"error": {"code": 404, "message": "Not Found"}}',
        '{"users": [{"id": 1, "name": "Alice"}]}'
    ],
    "XML": [
        "<root><item id=\"1\">Data</item></root>",
        "<?xml version=\"1.0\"?><book title=\"The Book\"></book>",
        "<user><name>Bob</name><age>40</age></user>",
        "<error code=\"500\">Internal error</error>",
        "<list><element>A</element><element>B</element></list>"
    ],
    "YAML": [
        "key: value\nlist:\n  - 1\n  - 2",
        "user:\n  name: Alice\n  age: 25",
        "config:\n  debug: true\n  port: 8080",
        "--- # Document Start\nproducts:\n  - Laptop",
        "settings: {timeout: 30, retries: 3}"
    ],
    "CSV": [
        "id,name,price\n1,Apple,1.00\n2,Banana,0.50",
        "Date,Open,High,Low,Close\n2023-01-01,100,105,98,103",
        "User,Action,Timestamp\nAlice,login,1672531200",
        "City;Population\nTokyo;13960000",
        "col1,col2\n\"data, with comma\",other data"
    ],
    "TOML": [
        "title = \"TOML Example\"\n\n[owner]\nname = \"Tom\"",
        "[server]\nip = \"127.0.0.1\"\nport = 8080",
        "data = [1, 2, 3]",
        "version = 1.0",
        "[config]\nmode = \"debug\""
    ],
    "INI": [
        "[DEFAULT]\nServerHost = 127.0.0.1\n\n[client]\nAPIKey = 12345",
        "[mysql]\nuser = root\npassword = secret",
        "[section]\nkey=value",
        "Timeout=30\nRetries=5",
        "log_file = /var/log/app.log"
    ],
    "Protocol Buffers": [
        "message Person { string name = 1; int32 id = 2; }",
        "syntax = \"proto3\";",
        "enum State { ACTIVE = 0; INACTIVE = 1; }",
        "repeated string emails = 3;",
        "import \"other.proto\";"
    ],
    "MessagePack": [
        "\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03",
        "\x82\xa4name\xa4John\xa3age\x1e",
        "\x81\xa5error\x82\xa4code\xce\x01\x90\xa7message\xa9Not Found",
        "\x91\x82\xa2id\x01\xa4name\xa5Alice",
        "\xc0\xc0\xc0\xc0\xc0"
    ],
    "Avro": [
        "{\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}]}",
        "\"type\": \"int\"",
        "\"default\": null",
        "\"doc\": \"A user record\"",
        "\"name\": \"event_time\", \"type\": \"long\""
    ],
    "BSON": [
        "\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00",
        "\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02",
        "\x03name\x00\x06\x00\x00\x00Bob\x00\x10age\x00\x28\x00\x00\x00",
        "\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08",
        "\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00"
    ],

    # --- Network/Protocol Data (10) ---
    "HTTP headers": [
        "GET / HTTP/1.1\nHost: example.com\nUser-Agent: curl/7.68.0",
        "POST /api/login HTTP/1.1\nContent-Type: application/json",
        "HTTP/1.1 200 OK\nContent-Length: 3495",
        "HTTP/1.1 404 Not Found\nContent-Type: text/html",
        "Authorization: Bearer token123\nAccept-Encoding: gzip, deflate"
    ],
    "TCP/IP packets": [
        "Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53",
        "Flags: [SYN], seq 0, win 64240, length 0",
        "IP Version 4, Header Length 20 bytes, TTL 64",
        "Protocol: TCP (6), Checksum: 0x1234 [correct]",
        "0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01"
    ],
    "DNS records": [
        "example.com. IN A 192.0.2.1",
        "www.example.com. IN CNAME example.com.",
        "example.com. IN MX 10 mail.example.com.",
        "example.com. IN TXT \"v=spf1 include:spf.google.com ~all\"",
        "ns1.example.com. IN NS example.com."
    ],
    "Email headers": [
        "From: \"Sender\" <sender@example.com>",
        "To: \"Recipient\" <recipient@example.com>",
        "Subject: Test Email",
        "Date: Mon, 1 Jan 2024 10:00:00 +0100",
        "Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)"
    ],
    "WebSocket frames": [
        "\x81\x05Hello",
        "\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c",
        "Opcode: Text (1)",
        "Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1",
        "Payload length: 5"
    ],
    "FTP commands": [
        "USER anonymous",
        "PASS guest@",
        "CWD /pub",
        "RETR file.zip",
        "220 FTP Server ready."
    ],
    "SSH logs": [
        "debug1: SSH2_MSG_KEXINIT sent",
        "Accepted publickey for user root from 1.2.3.4 port 50000 ssh2",
        "Connection closed by 1.2.3.4 [preauth]",
        "Disconnecting: Too many authentication failures",
        "session opened for user user by (uid=0)"
    ],
    "TLS handshake": [
        "Client Hello (1.2)",
        "Server Hello (1.2) [sid]",
        "Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
        "Certificate",
        "Change Cipher Spec"
    ],
    "REST API responses": [
        "Status: 200 OK\nContent-Type: application/json",
        '{"id": 1, "name": "API Item"}',
        "Status: 201 Created\nLocation: /api/items/2",
        "Status: 400 Bad Request\nError: Invalid input",
        '{"list": [1, 2, 3], "count": 3}'
    ],
    "GraphQL queries": [
        "query { user(id: 1) { name email } }",
        "mutation { createUser(name: \"New User\") { id } }",
        "fragment UserFields on User { name email }",
        "subscription { newNotification { message } }",
        "query GetProducts { products { id price } }"
    ],

    # --- Natural Language (Non-English) (10) ---
    "Spanish": [
        "Hola, ¿cómo estás? (Hello, how are you?)",
        "El sol es amarillo. (The sun is yellow.)",
        "Me gusta el chocolate. (I like chocolate.)",
        "¿Dónde está la biblioteca? (Where is the library?)",
        "Gracias por tu ayuda. (Thank you for your help.)"
    ],
    "French": [
        "Bonjour, comment ça va ?",
        "Il fait beau aujourd'hui.",
        "J'aime la cuisine française.",
        "Où sont les toilettes, s'il vous plaît ?",
        "Merci beaucoup."
    ],
    "German": [
        "Hallo, wie geht es Ihnen?",
        "Das Wetter ist schön.",
        "Ich spreche ein bisschen Deutsch.",
        "Wo ist der Bahnhof?",
        "Vielen Dank."
    ],
    "Chinese": [
        "你好，你怎么样？(Nǐ hǎo, nǐ zěnme yàng?)",
        "我是一个学生。(Wǒ shì yīgè xuésheng.)",
        "这是个测试。(Zhè shìgè cèshì.)",
        "再见，下次见。(Zàijiàn, xià cì jiàn.)",
        "北京很大。(Běijīng hěn dà.)"
    ],
    "Japanese": [
        "こんにちは、元気ですか？(Konnichiwa, genki desu ka?)",
        "私は学生です。(Watashi wa gakusei desu.)",
        "これはテストです。(Kore wa tesuto desu.)",
        "さようなら、また会いましょう。(Sayōnara, mata aimashō.)",
        "東京は大きいです。(Tōkyō wa ōkii desu.)"
    ],
    "Arabic": [
        "مرحبا، كيف حالك؟ (Marhaban, kayfa ḥāluk?)",
        "أنا بخير، شكراً. (Anā bikhayr, shukran.)",
        "الجو حار اليوم. (Al-jawwu ḥārr al-yawm.)",
        "من فضلك، ساعدني. (Min faḍlik, sā'idnī.)",
        "أين المتحف؟ (Ayna al-matḥaf?)"
    ],
    "Russian": [
        "Здравствуйте, как дела?",
        "Я говорю по-русски.",
        "Это очень важно.",
        "Сколько это стоит?",
        "До свидания."
    ],
    "Hindi": [
        "नमस्ते, आप कैसे हैं? (Namaste, aap kaise hain?)",
        "मुझे यह पसंद है। (Mujhe yah pasand hai.)",
        "मेरा नाम राहुल है। (Mera naam Rahul hai.)",
        "पानी कहाँ है? (Pānī kahāṁ hai?)",
        "धन्यवाद। (Dhan'yavād.)"
    ],
    "Portuguese": [
        "Olá, como você está?",
        "Eu amo o Brasil.",
        "Por favor, ajude-me.",
        "Onde é a praia?",
        "Muito obrigado."
    ],
    "Italian": [
        "Ciao, come stai?",
        "Io parlo italiano.",
        "È un bel giorno.",
        "Dov'è il bagno?",
        "Grazie mille."
    ],

    # --- Log/Error Messages (10) ---
    "Stack traces": [
        "File \"script.py\", line 10, in <module>\n  print(10 / 0)\nZeroDivisionError: division by zero",
        "Traceback (most recent call last):\n  File \"app.py\", line 5, in <module>\n    main()\nNameError: name 'undefined_var' is not defined",
        "java.lang.NullPointerException\n\tat com.example.MyClass.myMethod(MyClass.java:10)",
        "TypeError: Cannot read property 'length' of undefined\n    at app.js:5:10",
        "IndexError: list index out of range\n    at script.py:7"
    ],
    "System logs": [
        "Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted",
        "Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256",
        "Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something)",
        "Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user.",
        "Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254"
    ],
    "Application logs": [
        "[2023-12-14 10:00:00] INFO: App started successfully on port 8080",
        "[2023-12-14 10:00:01] DEBUG: Processing request for user 123",
        "[2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms)",
        "[2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied",
        "[2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down"
    ],
    "Security logs": [
        "ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4",
        "AUDIT: User 'john' modified configuration file /etc/config.conf",
        "FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22",
        "IDS: Potential SQL Injection detected in parameter 'q'",
        "USER_LOCKOUT: User 'test' locked out after 5 failed attempts"
    ],
    "Database logs": [
        "2023-12-14 10:00:00 LOG:  database system is ready to accept connections",
        "2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update",
        "2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1",
        "2023-12-14 10:00:03 WARNING:  non-optimal query execution plan",
        "2023-12-14 10:00:04 FATAL:  too many connections"
    ],
    "Web server logs": [
        "192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495",
        "10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120",
        "\"- \" \"Mozilla/5.0...\"",
        "\"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199",
        "\"HEAD /health HTTP/1.1\" 200 0"
    ],
    "Kernel logs": [
        "kernel: ACPI: button: Power Button [PWRF] present",
        "kernel: eth0: link up (1000Mbps/Full duplex)",
        "kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci",
        "kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\"",
        "kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child"
    ],
    "Crash dumps": [
        "Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0",
        "EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000",
        "Call stack:\n  0x401000 in main at main.c:10",
        "Memory status: Total: 8GB, Free: 1GB",
        "Reason: Access violation reading location 0x00000000"
    ],
    "Audit logs": [
        "type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"'",
        "type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null)",
        "type=AVC msg=audit(1671001202.000): avc:  denied  { read } for  pid=123 comm=\"bash\" name=\"test.txt\" dev=\"sda1\" ino=12345 scontext=...",
        "type=PROCTITLE msg=audit(1671001203.000): proctitle=2F7573722F62696E2F73736864002D44",
        "type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\""
    ],
    "Debug output": [
        "DEBUG: [Thread-1] Initializing service A...",
        "VERBOSE: Current state: IDLE, Value: 42",
        "TRACE: Function 'process_data' called with input: {'user': 'test'}",
        "DEBUG: Query took 15ms. SQL: SELECT * FROM table",
        "INFO: Configuration loaded from /etc/config.yml"
    ],

    # --- Placeholder/Lorem Ipsum (10) ---
    "Lorem Ipsum": [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa."
    ],
    "Fake names": [
        "Johnathan Smith",
        "Alice Johnson",
        "Robert Brown",
        "Emily Davis",
        "Michael Wilson"
    ],
    "Fake addresses": [
        "123 Fake St, Anytown, CA 90210",
        "45 Test Rd, Somewhere, NY 10001",
        "P.O. Box 789, Placeholder City, TX 77001",
        "Unit 10, Data Block, Virtual State, ZZ 11111",
        "987 Missing Ave, Noneburg, FL 33101"
    ],
    "Fake phone numbers": [
        "(555) 123-4567",
        "555-987-6543",
        "+1 555 111 2222",
        "555.000.4444",
        "1-555-555-1212"
    ],
    "Fake emails": [
        "john.smith@example.com",
        "alice.j@corpmail.net",
        "robert.b@fakedomain.org",
        "emily.davis@test.co",
        "michael.w@placeholder.io"
    ],
    "Fake company names": [
        "Acme Corp",
        "Globex Industries",
        "Initech Solutions",
        "Cyberdyne Systems",
        "Weyland-Yutani"
    ],
    "Fake product descriptions": [
        "The amazing gizmo-matic 5000: revolutionizing widget assembly since 2024.",
        "Quantum-laced trousers for enhanced mobility and style.",
        "A highly effective, non-toxic cleaner for all surfaces.",
        "This service provides zero-latency cloud storage for imaginary data.",
        "The next-generation communication device that runs on pure thought."
    ],
    "Fake reviews": [
        "5 stars: Simply the best! It changed my life.",
        "1 star: Arrived broken and the customer service was awful.",
        "3 stars: It's okay, but a bit overpriced for what you get.",
        "4 stars: Solid product, works as advertised. Highly recommend.",
        "2 stars: I was expecting more. Didn't solve my specific problem."
    ],
    "Fake social media posts": [
        "Just had the best coffee ever! #blessed #coffeeaddict",
        "Feeling sad today. Send good vibes. 😔",
        "OMG! You won't believe what happened at work today... 🤦‍♀️",
        "Check out my new puppy! He's so cute! [Image of puppy]",
    "Debating whether to order pizza or cook. What should I do? 🤔"
],

# --- Mixed/Edge Cases (10) ---
"Code + comments": [
    "// A simple loop\nfor i in range(10): # Loop 10 times\n    print(i) # Print the number",
    "/* C-style comment */\nint x = 10; // Inline comment",
    "# Python code with comments\n# Define a variable\nmy_var = 5",
    "\n<p>Text</p>",
    "// TODO: Fix this bug later\nreturn 0;"
],
"Markdown": [
    "# Heading 1\n\nThis is **bold** text and *italic* text.\n\n* List item 1\n* List item 2",
    "## Subheading\n\n```python\nprint('Code')\n```",
    "| Col1 | Col2 |\n|---|---|\n| Data1 | Data2 |",
    "> This is a blockquote.",
    "---"
],
"Template strings": [
    "`Hello, ${user.name}! You have ${notifications.count} messages.`",
    "f\"The result is {x/y:.2f}\"",
    "\"Name: {0}, Age: {1}\".format(name, age)",
    "<%= user.first_name %>",
    "{{ product.price | currency }}"
],
"Environment variables": [
    "DATABASE_URL=postgres://user:pass@host:port/db",
    "API_KEY=shh_its_a_secret",
    "NODE_ENV=production",
    "PORT=8080",
    "AWS_REGION=us-east-1"
],
"Configuration files": [
    "debug = True\nport = 8080\nhost = \"localhost\"",
    "[database]\ntype=postgres\nuser=admin\npassword=secret",
    "version: '3.8'\nservices:\n  web:\n    image: nginx",
    "server {\n  listen 80;\n  server_name example.com;\n}",
    "log_level: DEBUG\nmax_threads: 10"
],
"Dockerfiles": [
    "FROM python:3.9-slim",
    "WORKDIR /app",
    "COPY requirements.txt .",
    "RUN pip install -r requirements.txt",
    "CMD [\"python\", \"app.py\"]"
],
"Makefiles": [
    "all: clean compile test",
    "compile:\n\tgcc main.c -o app",
    "clean:\n\trm -f app *.o",
    ".PHONY: all clean",
    "test: app\n\t./app"
],
"Git diffs": [
    "--- a/file.txt\n+++ b/file.txt\n@@ -1,3 +1,4 @@\n-Hello\n+Hello World\n Clean\n New Line",
    "diff --git a/script.py b/script.py\nindex abcdef..123456 100644\n--- a/script.py\n+++ b/script.py\n@@ -1,5 +1,6 @@\n def func():\n-    return 1\n+    return 2",
    "--- a/config.json\n+++ b/config.json\n@@ -2,5 +2,5 @@\n-  \"port\": 8080\n+  \"port\": 9000",
    "deleted file mode 100644",
    "new file mode 100644"
],
"Code documentation": [
    "/**\n * Calculates the sum of two numbers.\n * @param {number} a - The first number.\n * @param {number} b - The second number.\n * @returns {number} The sum of a and b.\n */",
    "/// A function that prints a greeting to the console.\n/// # Example\n/// ```\n/// print_greeting(\"World\"); // Prints \"Hello, World!\"\n/// ```",
    "// Public: Returns the current user. (deprecated)",
    "@param name: str, the name of the user to greet",
    "@returns bool: True if successful, False otherwise"
],
"Inline HTML": [
    "This is normal text with a <span style=\"color: red;\">red word</span> inside.",
    "The date is <b>2024-01-01</b>.",
    "<code>print('Code')</code>",
    "<p>Line 1.<br>Line 2.</p>",
    "<a href=\"#\">Link</a>"
],

# --- Shell Scripting (10) ---
"Bash scripts": [
    "#!/bin/bash",
    "echo 'Hello, World!'",
    "grep -r error /var/log/ || echo 'No errors found'",
    "if [ -f file.txt ]; then cat file.txt; fi",
    "ps aux | grep python"
],
"PowerShell scripts": [
    "Write-Host \"Hello, PowerShell\"",
    "Get-Process | Where-Object {$_.CPU -gt 10}",
    "Start-Service -Name 'W32Time'",
    "if (-not (Test-Path $file)) { New-Item $file }",
    "$output = Invoke-WebRequest -Uri 'http://example.com'"
],
"Batch scripts": [
    "@echo off\necho Hello, Batch\npause",
    "if exist file.txt ( del file.txt )",
    "for %%i in (*.log) do echo %%i",
    "set VAR=test",
    "start chrome.exe"
],
"Shell one-liners": [
    "ls -l | awk '{print $NF}' | sort -u",
    "find . -name '*.log' -exec rm {} \\;",
    "curl -sL http://example.com | grep 'title'",
    "history | tail -n 10",
    "date +%Y-%m-%d"
],
"Cron jobs": [
    "0 1 * * * /usr/bin/backup.sh",
    "@reboot /usr/bin/start_service.sh",
    "*/5 * * * * /usr/bin/check_health",
    "# Run every Monday at 3am",
    "30 3 * * 1 /usr/bin/cleanup.py"
],
"Awk scripts": [
    "awk '{print $1}' data.txt",
    "awk '/error/ {count++} END {print count}' logfile.txt",
    "awk -F',' '{sum+=$2} END {print sum/NR}' data.csv",
    "awk 'NR==1, NR==5'",
    "awk '{gsub(/old/, \"new\", $0); print}'"
],
"Sed commands": [
    "sed 's/foo/bar/g' input.txt > output.txt",
    "sed '4d' file.txt",
    "sed -n '/start/,/end/p' file.txt",
    "sed '/^#/d' file.txt",
    "sed 's/^/prefix_/' file.txt"
],
"Grepping logs": [
    "grep -i 'fatal error' system.log",
    "grep -E '^(WARNING|ERROR)' app.log",
    "grep -v 'ignored' debug.log",
    "grep -c 'success' history.log",
    "grep 'PID' /var/log/messages"
],
"Piping commands": [
    "cat file1.txt | less",
    "echo 'data' | tr 'a-z' 'A-Z'",
    "ls -l | wc -l",
    "find . -type f | xargs grep 'pattern'",
    "head -n 10 log.txt | tail -n 1"
],
"Redirecting output": [
    "echo 'log entry' >> app.log",
    "command < input.txt > output.txt 2>&1",
    "ls > file_list.txt",
    "cat < file.txt",
    "command 2> error.log"
],

# --- Config Files (10) ---
"JSON config": [
    '{"server": {"port": 8080, "host": "0.0.0.0"}}',
    '{"database": {"url": "postgres://user:pass@localhost:5432/db"}}',
    '{"logging": {"level": "debug", "file": "app.log"}}',
    '{"features": ["auth", "logging", "metrics"]}',
    '{"timeout": 30, "retries": 3}'
],
"YAML config": [
    "database:\n  adapter: postgres\n  host: db.server.com",
    "users:\n  - name: Alice\n  - name: Bob",
    "services:\n  api: {port: 5000}",
    "environment: production\nlogging_level: INFO",
    "--- # Separator"
],
"INI config": [
    "[DEFAULT]\nServerHost = 127.0.0.1\n\n[client]\nAPIKey = 12345",
    "[mysql]\nuser = root\npassword = secret",
    "[section]\nkey=value",
    "Timeout=30\nRetries=5",
    "log_file = /var/log/app.log"
],
"TOML config": [
    "title = \"TOML Example\"\n\n[owner]\nname = \"Tom\"",
    "[server]\nip = \"127.0.0.1\"\nport = 8080",
    "data = [1, 2, 3]",
    "version = 1.0",
    "[config]\nmode = \"debug\""
],
"XML config": [
    "<config><logging enabled=\"true\" level=\"INFO\"></logging></config>",
    "<app-settings><key name=\"Host\">localhost</key></app-settings>",
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
    "<resources><string name=\"app_name\">My App</string></resources>",
    "<database><connection string=\"user=a;pass=b\"></database>"
],
"Properties files": [
    "app.name=My Application",
    "server.port=8080",
    "db.username=root",
    "# Comments are allowed",
    "log4j.rootLogger=INFO, stdout"
],
"Environment files": [
    "DEBUG=1",
    "SECRET_KEY=long_random_string_here",
    "PORT=3000",
    "TEST_MODE=False",
    "DATABASE_URL=sqlite:///db.sqlite"
],
"Nginx config": [
    "server {\n  listen 80;\n  server_name example.com;\n  root /var/www/html;\n}",
    "location /api/ {\n  proxy_pass http://backend:8080;\n}",
    "ssl_certificate /etc/ssl/cert.pem;",
    "error_page 500 502 /50x.html;",
    "access_log /var/log/nginx/access.log;"
],
"Apache config": [
    "<VirtualHost *:80>\n  ServerName example.com\n  DocumentRoot /var/www/html\n</VirtualHost>",
    "LoadModule rewrite_module modules/mod_rewrite.so",
    "RewriteEngine On\nRewriteRule ^/oldurl /newurl [R=301,L]",
    "ErrorLog ${APACHE_LOG_DIR}/error.log",
    "LogLevel warn"
],
"Docker Compose": [
    "version: '3.8'\nservices:\n  web:\n    image: nginx:latest",
    "  db:\n    image: postgres:14-alpine\n    environment:\n      - POSTGRES_USER=user",
    "volumes:\n  data: {} # Empty volume",
    "networks:\n  default: { driver: bridge }",
    "ports:\n  - \"80:80\""
],

# --- Spam/Advertisement Text (10) ---
"Email spam": [
    "WIN A FREE IPHONE! Click here: http://bit.ly/12345",
    "You've been selected for a $1000 gift card! Claim now: http://example.com",
    "URGENT: Your account has been compromised. Click to secure: http://fake.link",
    "Congratulations! You've won a vacation. Reply to claim your prize.",
    "Limited time offer: 50% off all products! Shop now: http://scam.site"
],
"SMS spam": [
    "FINAL NOTICE: Your USPS delivery is pending. Schedule a drop-off here: [link]",
    "Free ringtone! Text YES to 12345. $9.99/week charges apply.",
    "Hi [Name], it's your bank. We noticed suspicious activity. Call this number now: 800-555-1212",
    "You won a contest! Claim your prize: http://tinyurl.com/prize",
    "Discount code: GET50NOW. Limited stock! Don't miss out!"
],
"Pop-up ads": [
    "WARNING! Your computer is infected! Click here to clean it now.",
    "Enter your email to get a free eBook!",
    "You are the 1,000,000th visitor! Claim your reward!",
    "Click ALLOW to receive notifications from this site.",
    "This article is sponsored by [Brand Name]. Buy Now!"
],
"Phishing messages": [
    "Your PayPal account has been locked. Verify your identity at: http://phishing.link",
    "Amazon: Your order #12345 could not be delivered. Update address here: http://fake-amazon.com",
    "Last chance! Your Netflix payment failed. Update billing info now to prevent service interruption: http://fake-netflix.net",
    "We detected an unauthorized login attempt. Change your password here immediately: http://security-alert.org",
    "IRS Tax Refund Pending. Click here to submit your details: http://irs-refund.net"
],
"Scam offers": [
    "Make $5,000 a week working from home! No experience necessary!",
    "Invest $100 today and turn it into $10,000 by tomorrow!",
    "Get a free trial of our miracle diet pill!",
    "Urgent investment opportunity: cryptocurrency is exploding!",
    "You have inherited $10 million from a long-lost relative!"
],
"Fake promotions": [
    "Flash Sale! Everything 90% off for the next 5 minutes!",
    "Two-for-one deal on imaginary products!",
    "Today only: free shipping on all orders over $0!",
    "Limited edition item, selling out fast!",
    "Be the first 100 people to sign up and get a bonus!"
],
"Clickbait": [
    "You Won't BELIEVE What Happened When She Tried THIS ONE WEIRD TRICK!",
    "Doctors HATE Her! Learn The Secret To A Flat Belly!",
    "The #1 Thing Everyone Is Talking About!",
    "He Thought It Was Over, But Then...",
    "10 Photos That Prove Time Travel Is Real (Number 7 Will Shock You!)"
],
"Malware warnings": [
    "Threat Detected: Trojan-42. Delete immediately by clicking OK.",
    "Your files are encrypted. Pay 1.0 Bitcoin to restore them.",
    "Security Alert: Your license key has expired. Download the update.",
    "The webpage you are attempting to view contains malware.",
    "Warning: This file may harm your computer."
],
"Chain letters": [
    "Send this to 10 friends or you will have bad luck for 7 years!",
    "If you don't share this post, the internet will crash.",
    "A little girl is dying of cancer. Forward this email to raise money.",
    "This is an important message from the founder of [Platform].",
    "The secret to happiness is revealed in the final line (forward to 5 people)."
],
"Survey scams": [
    "Fill out this survey for a chance to win a free MacBook!",
    "Tell us about your shopping experience and get a $50 gift card.",
    "Answer 3 quick questions to unlock a secret discount!",
    "Congratulations! You've been chosen for a special consumer study.",
    "Your opinion matters! Click here to participate in our poll."
],

# --- ASCII Art (10) ---
"Simple art": [
    " /\_/\\ \n( o.o )\n > ^ <",
    "  _____  \n /       \\ \n|  X   X  |\n|   ••   |\n \\_____/  ",
    "  ^__^  \n (oo)\_______ \n(__)\       )\/\\ \n    ||----w |",
    "  .----.  \n /      \\ \n|  O  O  |\n|    ∆   |\n \\      / ",
    "  (\___/)  \n  (•ㅅ•)  \n  /  ❤️  \\  \n (   ( )   )"
],
"Complex art": [
    "                     ( (\n                       ) )\n  .---.   .---.   .---.   ( (\n /     \\ /     \\ /     \\  ) )",
    "               \\|//\n             /|o O|\\\n             \\\\_^_/\n            --\\ | /--",
    "  ( (\n   ) )\n  ( (\n   ) )",
    "                 _.-'\n               .'\n              /"
],
"Text-based games": [
    "You are in a forest. To the North is a cave. To the East is a river. What do you do?",
    "Inventory:\n- Sword (rusty)\n- Torch (dim)\n- Apple (1)",
    "*** ZORK I: The Great Underground Empire ***\n(c) 1981 Infocom, Inc.\n\nWest of House\nYou are standing in an open field west of a white house.",
    "You lost 5 HP. Remaining HP: 15/20.",
    "Choose your action:\n[A] Attack\n[B] Run\n[C] Inventory"
],
"Banners": [
    "#########################\n#  WELCOME TO THE APP!  #\n#########################",
    "*************************\n* WARNING!        *\n*************************",
    "=========================\n  SYSTEM INITIALIZED\n=========================",
    "--- START ---",
    "+++ END OF LOG +++"
],
"Emoticon art": [
    "༼ つ ◕_◕ ༽つ",
    "(╯°□°）╯︵ ┻━┻",
    "¯\\_(ツ)_/¯",
    "( ͡° ͜ʖ ͡°)",
    "😂🤣😭👍"
],
"Diagrams": [
    "    A\n   / \\\n  B---C",
    "  +--[Start]\n  | \n  v\n [Process]--->[End]",
    "  (Input) --> [Function] --> (Output)",
    "  [Client] <--> [Server]",
    "  [Data] | [Model] | [Result]"
],
"Tables": [
    "+------+--------+\n| ID   | Name   |\n+------+--------+\n| 1    | Alice  |\n| 2    | Bob    |\n+------+--------+",
    "| Header 1 | Header 2 |\n|----------|----------|\n| Data A   | Data B   |",
    "Key: Value\n---\nSize: 10\nColor: Red",
    "------------------\nName\tAge\tCity\nAlice\t30\tNY\n------------------",
    "| Cat | Dog | Fish |\n|-----|-----|------|\n| 3   | 2   | 10   |"
],
"Flowcharts": [
    "START -> Input Data -> Process Data -> Output Result -> END",
    "IF (Condition) THEN (Action 1) ELSE (Action 2)",
    "Loop: Initialization -> Condition Check -> Body -> Update -> Exit",
    "A -> B -> C",
    "Decision? -> Yes -> Action Y | No -> Action N"
],
"Memes": [
    "One does not simply\nwalk into Mordor.",
    "All your base are belong to us.",
    "Doge: such code, much wow, very error.",
    "The most interesting man in the world: I don't always use Python, but when I do, I use Python 3.",
    "Disappointed GIF text: You had one job."
],
"Text-based UI": [
    "┌──────────────────────┐\n│      MAIN MENU       │\n├──────────────────────┤\n│ 1. Start             │\n│ 2. Settings          │\n│ 3. Exit              │\n└──────────────────────┘",
    "( ) Option 1\n(X) Option 2",
    "[OK] [Cancel]",
    "Loading...\n[##########] 100%",
    "Username: [__________]\nPassword: [__________]"
]
}


def get_off_topic_texts():
    off_topic_texts = []
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            examples = simplified_example_templates.get(subcategory, [])
            off_topic_texts.extend(examples[:5])

    # Shuffle the list to mix categories
    seeded_random = random.Random(42)
    seeded_random.shuffle(off_topic_texts)

    return off_topic_texts

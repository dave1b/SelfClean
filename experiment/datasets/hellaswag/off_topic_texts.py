import random

# Redefine the categories to focus on severe off-topic content
categories = {
    "Non-readable/Gibberish": [
        "Random characters", "Unicode/Emoji mix", "Keyboard smashes",
        "Base64 encoded", "URL-encoded", "Hex dump", "Binary data",
        "Mixed symbols"
    ],
    "Bytecode/Compiled Output": [
        "Python bytecode", "Java bytecode", "Assembly",
        "LLVM IR", "WebAssembly", "JVM bytecode",
        ".NET IL", "Machine code", "Disassembly", "Obfuscated code"
    ],
    "Mathematical/Scientific Notation": [
        "LaTeX", "Chemical formulas",
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
    "Log/Error Messages": [
        "Stack traces", "System logs", "Application logs",
        "Security logs", "Database logs", "Web server logs",
        "Kernel logs", "Crash dumps", "Audit logs"
    ],
    "Shell Scripting": [
        "Bash scripts", "PowerShell scripts", "Batch scripts",
        "Shell one-liners", "Cron jobs", "Awk scripts",
        "Sed commands", "Grepping logs", "Piping commands", "Redirecting output"
    ],
}

# --- Expanded and more severe off-topic templates ---
expanded_example_templates = {
    # --- Non-readable/Gibberish ---
    "Random characters": [
        "asdfjkl;qwer!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./",
        "zxcvbnm,./!@#$%^&*()_+qwertyuiopasdfghjklzxcvbnm,./!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./",
        "1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./",
        "!@#$%^&*()_+qwertyuiopasdfghjklzxcvbnm,./!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./",
        "poiuytrewq!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./!@#$%^&*()_+1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnm,./"
    ],
    "Unicode/Emoji mix": [
        "🚀🌕💻🔥📱🎮🌍🌟💡🔑🚀🌕💻🔥📱🎮🌍🌟💡🔑🚀🌕💻🔥📱🎮🌍🌟💡🔑🚀🌕💻🔥📱🎮🌍🌟💡🔑🚀🌕💻🔥📱🎮🌍🌟💡🔑🚀🌕💻🔥📱🎮🌍🌟💡🔑",
        "😀😃😄😁😆😅😂🤣😊😇😀😃😄😁😆😅😂🤣😊😇😀😃😄😁😆😅😂🤣😊😇😀😃😄😁😆😅😂🤣😊😇😀😃😄😁😆😅😂🤣😊😇",
        "🌈🌟🌠🌦️🌧️☔️⛈️🌩️🌈🌟🌠🌦️🌧️☔️⛈️🌩️🌈🌟🌠🌦️🌧️☔️⛈️🌩️🌈🌟🌠🌦️🌧️☔️⛈️🌩️🌈🌟🌠🌦️🌧️☔️⛈️🌩️",
        "🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭🍎🍌🍉🍊🍋🍓🍈🍒🍑🥭",
        "🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮🎵🎶🎹🎻🎺🎷🥁🎲🎯🎮"
    ],
    "Keyboard smashes": [
        "gjhgjhkjghkjhghjlkjhlkgjhgjhkjghkjhghjlkjhlkgjhgjhkjghkjhghjlkjhlkgjhgjhkjghkjhghjlkjhlkgjhgjhkjghkjhghjlkjhlk",
        "qweqweasdzxccxzxcvasdqweqweasdzxccxzxcvasdqweqweasdzxccxzxcvasdqweqweasdzxccxzxcvasdqweqweasdzxccxzxcvasd",
        "!!!!!!!!!???????????!!!!!!!!!???????????!!!!!!!!!???????????!!!!!!!!!???????????!!!!!!!!!???????????",
        "................!!!!................!!!!................!!!!................!!!!................!!!!",
        "zxcmnbjhvcfgdfgcvbzxcmnbjhvcfgdfgcvbzxcmnbjhvcfgdfgcvbzxcmnbjhvcfgdfgcvbzxcmnbjhvcfgdfgcvbzxcmnbjhvcfgdfgcvb"
    ],
    "Base64 encoded": [
        "SGVsbG8gV29ybGQgSGVsbG8gV29ybGQgSGVsbG8gV29ybGQgSGVsbG8gV29ybGQgSGVsbG8gV29ybGQgSGVsbG8gV29ybGQgSGVsbG8gV29ybGQ=",
        "QWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8kQWJjMTIzIT8k",
        "VGhpcyBpcyBhIHRlc3QgVGhpcyBpcyBhIHRlc3QgVGhpcyBpcyBhIHRlc3QgVGhpcyBpcyBhIHRlc3QgVGhpcyBpcyBhIHRlc3QgVGhpcyBpcyBhIHRlc3Q=",
        "ZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9SZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9SZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9SZGF0YTppbWFnZS9wbmc7YmFzZTY0LGlWQk9S",
        "RGFzayBpcyBvZnRlbiB1c2VkIERhc2sgaXMgb2Z0ZW4gdXNlZCBEYXNrIGlzIG9mdGVuIHVzZWQgRGFzayBpcyBvZnRlbiB1c2VkIERhc2sgaXMgb2Z0ZW4gdXNlZCBEYXNrIGlzIG9mdGVuIHVzZWQ="
    ],
    "URL-encoded": [
        "key%3Dvalue%26param%3D1%26another%3Dtest%26more%3Ddata%26key%3Dvalue%26param%3D1%26another%3Dtest%26more%3Ddata%26key%3Dvalue%26param%3D1%26another%3Dtest%26more%3Ddata",
        "Hello%2C%20World%21%20Hello%2C%20World%21%20Hello%2C%20World%21%20Hello%2C%20World%21%20Hello%2C%20World%21",
        "file%2Fpath%2Fto%2Fresource%2Ffile%2Fpath%2Fto%2Fresource%2Ffile%2Fpath%2Fto%2Fresource%2Ffile%2Fpath%2Fto%2Fresource",
        "%C3%A9cole%20%C3%A0%20Paris%C3%A9cole%20%C3%A0%20Paris%C3%A9cole%20%C3%A0%20Paris%C3%A9cole%20%C3%A0%20Paris%C3%A9cole%20%C3%A0%20Paris",
        "search%3Dquery%26limit%3D10%26offset%3D20%26sort%3Ddesc%26search%3Dquery%26limit%3D10%26offset%3D20%26sort%3Ddesc"
    ],
    "Hex dump": [
        "0000 7a 78 63 76 62 6e 6d 20 31 32 33 0a 0000 7a 78 63 76 62 6e 6d 20 31 32 33 0a 0000 7a 78 63 76 62 6e 6d 20 31 32 33 0a 0000 7a 78 63 76 62 6e 6d 20 31 32 33 0a",
        "48 65 6c 6c 6f 20 57 6f 72 6c 64 21 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 48 65 6c 6c 6f 20 57 6f 72 6c 64 21",
        "0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 0d",
        "f0 9f 9a 80 e2 9c a8 61 73 64 66 f0 9f 9a 80 e2 9c a8 61 73 64 66 f0 9f 9a 80 e2 9c a8 61 73 64 66 f0 9f 9a 80 e2 9c a8 61 73 64 66",
        "c3 a9 c3 a8 c3 a0 c3 b9 c3 b2 c3 a9 c3 a8 c3 a0 c3 b9 c3 b2 c3 a9 c3 a8 c3 a0 c3 b9 c3 b2 c3 a9 c3 a8 c3 a0 c3 b9 c3 b2"
    ],
    "Binary data": [
        "01001000 01100101 01101100 01101100 01101111 01001000 01100101 01101100 01101100 01101111 01001000 01100101 01101100 01101100 01101111 01001000 01100101 01101100 01101100 01101111",
        "10101010 01010101 11110000 00001111 10101010 01010101 11110000 00001111 10101010 01010101 11110000 00001111 10101010 01010101 11110000 00001111",
        "00000001 00000010 00000011 00000100 00000001 00000010 00000011 00000100 00000001 00000010 00000011 00000100 00000001 00000010 00000011 00000100",
        "11111111 11111111 00000000 00000000 11111111 11111111 00000000 00000000 11111111 11111111 00000000 00000000 11111111 11111111 00000000 00000000",
        "01101110 01100001 01101110 01101110 01100001 01101110 01100001 01101110 01100001 01101110 01100001 01101110 01100001 01101110 01100001 01101110 01100001"
    ],
    "Mixed symbols": [
        "##@!$%.^&**()_+-={}I[]\\<>?//##@!$%.^&**()_+-={}I[]\\<>?//##@!$%.^&**()_+-={}I[]\\<>?//##@!$%.^&**()_+-={}I[]\\<>?//",
        "~~~`I!@#$%^&*()_+~~~`I!@#$%^&*()_+~~~`I!@#$%^&*()_+~~~`I!@#$%^&*()_+~~~`I!@#$%^&*()_+",
        "&^%#@!.>~&^%#@!.>~&^%#@!.>~&^%#@!.>~&^%#@!.>~&^%#@!.>~&^%#@!.>~&^%#@!.>~",
        "[1+2]*3/(4-5)[1+2]*3/(4-5)[1+2]*3/(4-5)[1+2]*3/(4-5)[1+2]*3/(4-5)",
        "<>[]{}()I\\<>[]{}()I\\<>[]{}()I\\<>[]{}()I\\<>[]{}()I\\"
    ],

    # --- Bytecode/Compiled Output ---
    "Python bytecode": [
        "2 0 LOAD_GLOBAL              0 (print) 2 LOAD_CONST               1 (None) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n) 2 0 LOAD_GLOBAL              0 (print) 2 LOAD_CONST               1 (None) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n)",
        "4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n)",
        "12 LOAD_CONST               2 (1)14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial)22 LOAD_FAST                0 (n)2 0 LOAD_GLOBAL              0 (print) 2 LOAD_CONST               1 (None) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n)",
        "20 LOAD_GLOBAL              1 (factorial)22 LOAD_FAST                0 (n)2 0 LOAD_GLOBAL              0 (print) 2 LOAD_CONST               1 (None) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n)",
        "22 LOAD_FAST                0 (n)2 0 LOAD_GLOBAL              0 (print) 2 LOAD_CONST               1 (None) 4 LOAD_FAST                0 (n) 6 LOAD_CONST               2 (1) 8 COMPARE_OP               1 (<=) 10 POP_JUMP_IF_FALSE       20 12 LOAD_CONST               2 (1) 14 RETURN_VALUE 20 LOAD_GLOBAL              1 (factorial) 22 LOAD_FAST                0 (n)"
    ],
    "Java bytecode": [
        "0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return 0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return 0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return",
        "4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1",
        "iconst_0 istore_1 0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1",
        "7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1 0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1",
        "9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1 0: aload_01: invokespecial #1 // Method java/lang/Object.\"<init>\":()V 4: getstatic #2 // Field java/lang/System.out:Ljava/io/PrintStream; 7: ldc #3 // String Hello 9: invokevirtual #4 // Method java/io/PrintStream.println:(Ljava/lang/String;)V 12: return iconst_0 istore_1"
    ],
    "Assembly": [
        "MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET",
        "JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET",
        "PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET",
        "CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET",
        "RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET MOV EAX, 1 JMP LABEL_LOOP PUSH EBP CALL _printf RET"
    ],
    "LLVM IR": [
        "define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond",
        "%1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond",
        "call void @print_int(i32 %1) br label %loop_cond define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond",
        "br label %loop_cond define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond",
        "define i32 @main() #0 { ret i32 0 } %1 = alloca i32, align 4 store i32 5, i32* %1, align 4 call void @print_int(i32 %1) br label %loop_cond define i32 @main() #0 { ret i32 0 }"
    ],
    "WebAssembly": [
        "(module (func (export \"add\") (param $a i32) (param $b i32) (result i32)   local.get $a   local.get $b   i32.add)) (module (func (export \"add\") (param $a i32) (param $b i32) (result i32)   local.get $a   local.get $b   i32.add)) (module (func (export \"add\") (param $a i32) (param $b i32) (result i32)   local.get $a   local.get $b   i32.add))",
        "i32.const 42 local.set $result call $print i32.const 42 local.set $result call $print i32.const 42 local.set $result call $print",
        "local.set $result call $print i32.const 42 local.set $result call $print i32.const 42 local.set $result call $print i32.const 42",
        "call $print i32.const 42 local.set $result call $print i32.const 42 local.set $result call $print i32.const 42 local.set $result",
        "loop $L0 (module (func (export \"add\") (param $a i32) (param $b i32) (result i32)   local.get $a   local.get $b   i32.add)) (module (func (export \"add\") (param $a i32) (param $b i32) (result i32)   local.get $a   local.get $b   i32.add))"
    ],
    "JVM bytecode": [
        "aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd",
        "ldc \"Hello\ astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd",
        "iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass",
        "astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass",
        "iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\ astore_1 iload_1iconst_1iadd aload_0 invokevirtual java/lang/Object.getClass ldc \"Hello\""
    ],
    ".NET IL": [
        "IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret IL_0010: ldloc.0 IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret IL_0010: ldloc.0",
        "IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret IL_0010: ldloc.0 IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string)",
        "IL_000a: nop IL_000b: ret IL_0010: ldloc.0 IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret",
        "IL_000b: ret IL_0010: ldloc.0 IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret IL_0010: ldloc.0",
        "ldloc.0 IL_0000: ldstr \"Hello World\ IL_0005: call void [mscorlib]System.Console::WriteLine(string) IL_000a: nop IL_000b: ret IL_0010: ldloc.0 IL_0000: ldstr \"Hello World\""
    ],
    "Machine code": [
        "55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3 55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3",
        "B8 01 00 00 00 C3 E8 00 00 00 00 5D C3 55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3 B8 01 00 00 00 C3",
        "E8 00 00 00 00 5D C3 55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3 E8 00 00 00 00 5D C3",
        "89 E5 83 C4 08 C9 C3 55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3 89 E5 83 C4 08 C9 C3",
        "48 83 C4 08 C3 55 89 E5 83 EC 10 C7 45 FC 00 00 00 00 E8 B8 01 00 00 00 C3 48 83 C4 08 C3"
    ],
    "Disassembly": [
        "0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start> 0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start>",
        "0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start> 0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp",
        "0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start> 0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp)",
        "0x40100f <main+15>: callq  0x400000 <_start> 0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start>",
        "<main+15>: callq  0x400000 <_start> 0x401000 <main+0>: push   %rbp 0x401001 <main+1>: mov    %rsp,%rbp 0x401004 <main+4>: sub    $0x10,%rsp 0x401008 <main+8>: movl   $0x0,-0x4(%rbp) 0x40100f <main+15>: callq  0x400000 <_start>"
    ],
    "Obfuscated code": [
        "eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};...eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};...eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};...eval(function(p,a,c,k,e,r){e=function(c){return c.toString(36)};...",
        "var _0x4e21=['test','123','join','split']; (function(_0x5c4115,_0x4e2124){...var _0x4e21=['test','123','join','split']; (function(_0x5c4115,_0x4e2124){...var _0x4e21=['test','123','join','split']; (function(_0x5c4115,_0x4e2124){...",
        "const _0x1a8b = ['\x63\x6f\x6e\x73\x6f\x6c\x65', '\x6c\x6f\x67', '\x48\x65\x6c\x6c\x6f'];const _0x1a8b = ['\x63\x6f\x6e\x73\x6f\x6c\x65', '\x6c\x6f\x67', '\x48\x65\x6c\x6c\x6f'];const _0x1a8b = ['\x63\x6f\x6e\x73\x6f\x6c\x65', '\x6c\x6f\x67', '\x48\x65\x6c\x6c\x6f'];",
        "function a(b){return b-1}function a(b){return b-1}function a(b){return b-1}function a(b){return b-1}",
        "var x=0x10; while(x>0){x--}var x=0x10; while(x>0){x--}var x=0x10; while(x>0){x--}var x=0x10; while(x>0){x--}"
    ],

    # --- Mathematical/Scientific Notation ---
    "LaTeX": [
        "$\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$ $\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$",
        "$$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$ $\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$",
        "$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$ $\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$",
        "$\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$ $\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$",
        "$\\mathbf{A} \\vec{x} = \\vec{b}$ $\\int_0^1 x^2 dx$ $$\\frac{d}{dx} e^x = e^x$$ $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$ $\\alpha \\beta \\gamma \\delta$ $\\mathbf{A} \\vec{x} = \\vec{b}$"
    ],
    "Chemical formulas": [
        "H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2",
        "C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2",
        "NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2",
        "H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2",
        "CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2 H2O C6H12O6 NaCl H2SO4 CO2"
    ],
    "Physics formulas": [
        "$\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law) $\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law)",
        "$\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law) $\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law)",
        "$\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law) $\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law)",
        "$T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law) $\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law)",
        "$V = IR$ (Ohm's law) $\vec{F} = q(\vec{E} + \vec{v} \\times \vec{B})$ (Lorentz force) $\\lambda = h / p$ (de Broglie wavelength) $\Delta x \Delta p \\ge \hbar/2$ (Heisenberg uncertainty) $T = 2\pi\sqrt{L/g}$ (Pendulum period) $V = IR$ (Ohm's law)"
    ],
    "Statistical notation": [
        "$P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$ $P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$",
        "$\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$ $P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$",
        "$Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$ $P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$",
        "$H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$ $P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$",
        "$R^2 = 1 - (SS_{res} / SS_{tot})$ $P(AIB) = \\frac{P(BIA)P(A)}{P(B)}$ (Bayes' theorem) $\\bar{x} = \\frac{1}{n} \\sum_{i=1}^n x_i$ $Z = (X - \mu) / \sigma$ $H_0: \mu = 0$ (Null hypothesis) $R^2 = 1 - (SS_{res} / SS_{tot})$"
    ],
    "Algebraic expressions": [
        "$(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$ $(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$",
        "$\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$ $(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$",
        "$3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$ $(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$",
        "$(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$ $(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$",
        "$2(z + 3) - 7 = 9$ $(x+y)^2 = x^2 + 2xy + y^2$ $\\frac{x}{2} + 5 = 10$ $3x^2 - 4x + 1$ $(a^2 - b^2) / (a - b) = a + b$ $2(z + 3) - 7 = 9$"
    ],
    "Calculus": [
        "$\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$ $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$",
        "$\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$ $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$",
        "$\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$ $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$",
        "$\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$ $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$",
        "$\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$ $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$ $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ $\\frac{\partial f}{\partial x}$ $\ abla^2 V = 0$ (Laplace's equation) $\\frac{d}{dt} \int_a^{t} f(x) dx = f(t)$"
    ],
    "Logic": [
        "P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$ P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$",
        "$\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$ P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$",
        "$\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$ P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$",
        "$(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$ P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$",
        "$(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$ P $\\rightarrow$ Q $\ eg (A \land B) \equiv  eg A \lor  eg B$ $\forall x (P(x) \rightarrow Q(x))$ $(P \lor  eg P) \equiv \top$ (Law of excluded middle) $(A \Rightarrow B) \land (B \Rightarrow C) \Rightarrow (A \Rightarrow C)$"
    ],
    "Set theory": [
        "$A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$ $A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$",
        "$x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$ $A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$",
        "$A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$ $A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$",
        "$\mathcal{P}(S)$ (Power set) $ISI = n$ $A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$",
        "$ISI = n$ $A \cup B$ $x \in \mathbb{R}$ $A \subseteq B \iff \forall x (x \in A \rightarrow x \in B)$ $\mathcal{P}(S)$ (Power set) $ISI = n$"
    ],
    "Matrix notation": [
        "$$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$ $$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$",
        "$\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$ $$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$",
        "$\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$ $$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$",
        "$\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$ $$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$",
        "$\\mathbf{A}^T$ $$\mathbf{A} = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}$$ $\\mathbf{A} \mathbf{x} = \mathbf{b}$ $\\det(\mathbf{A})$ $\\mathbf{I}$ (Identity matrix) $\\mathbf{A}^T$"
    ],

    # --- Data Serialization Formats ---
    "JSON": [
        '{"key": "value", "array": [1, 2, 3], "nested": {"a": 1, "b": 2}, "list": [{"id": 1}, {"id": 2}]} {"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}} {"status": "success", "data": {"id": 123, "items": [1, 2, 3]}} {"error": {"code": 404, "message": "Not Found", "details": {"field": "name", "value": null}}} {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}',
        '{"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}} {"status": "success", "data": {"id": 123, "items": [1, 2, 3]}} {"error": {"code": 404, "message": "Not Found", "details": {"field": "name", "value": null}}} {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]} {"key": "value", "array": [1, 2, 3], "nested": {"a": 1, "b": 2}, "list": [{"id": 1}, {"id": 2}]}',
        '{"status": "success", "data": {"id": 123, "items": [1, 2, 3]}} {"error": {"code": 404, "message": "Not Found", "details": {"field": "name", "value": null}}} {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]} {"key": "value", "array": [1, 2, 3], "nested": {"a": 1, "b": 2}, "list": [{"id": 1}, {"id": 2}]} {"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}}',
        '{"error": {"code": 404, "message": "Not Found", "details": {"field": "name", "value": null}}} {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]} {"key": "value", "array": [1, 2, 3], "nested": {"a": 1, "b": 2}, "list": [{"id": 1}, {"id": 2}]} {"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}} {"status": "success", "data": {"id": 123, "items": [1, 2, 3]}}',
        '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]} {"key": "value", "array": [1, 2, 3], "nested": {"a": 1, "b": 2}, "list": [{"id": 1}, {"id": 2}]} {"name": "John", "age": 30, "city": "New York", "address": {"street": "123 Main St", "zip": "10001"}} {"status": "success", "data": {"id": 123, "items": [1, 2, 3]}} {"error": {"code": 404, "message": "Not Found", "details": {"field": "name", "value": null}}}'
    ],
    "XML": [
        "<root><item id=\"1\">Data</item><item id=\"2\">More Data</item></root> <?xml version=\"1.0\"?><book title=\"The Book\"><chapter>One</chapter><chapter>Two</chapter></book> <user><name>Bob</name><age>40</age><address><street>123 Main</street></address></user> <error code=\"500\"><message>Internal error</message><details>Stack trace here</details></error> <list><element>A</element><element>B</element><element>C</element></list>",
        "<?xml version=\"1.0\"?><book title=\"The Book\"><chapter>One</chapter><chapter>Two</chapter></book> <user><name>Bob</name><age>40</age><address><street>123 Main</street></address></user> <error code=\"500\"><message>Internal error</message><details>Stack trace here</details></error> <list><element>A</element><element>B</element><element>C</element></list> <root><item id=\"1\">Data</item><item id=\"2\">More Data</item></root>",
        "<user><name>Bob</name><age>40</age><address><street>123 Main</street></address></user> <error code=\"500\"><message>Internal error</message><details>Stack trace here</details></error> <list><element>A</element><element>B</element><element>C</element></list> <root><item id=\"1\">Data</item><item id=\"2\">More Data</item></root> <?xml version=\"1.0\"?><book title=\"The Book\"><chapter>One</chapter><chapter>Two</chapter></book>",
        "<error code=\"500\"><message>Internal error</message><details>Stack trace here</details></error> <list><element>A</element><element>B</element><element>C</element></list> <root><item id=\"1\">Data</item><item id=\"2\">More Data</item></root> <?xml version=\"1.0\"?><book title=\"The Book\"><chapter>One</chapter><chapter>Two</chapter></book> <user><name>Bob</name><age>40</age><address><street>123 Main</street></address></user>",
        "<list><element>A</element><element>B</element><element>C</element></list> <root><item id=\"1\">Data</item><item id=\"2\">More Data</item></root> <?xml version=\"1.0\"?><book title=\"The Book\"><chapter>One</chapter><chapter>Two</chapter></book> <user><name>Bob</name><age>40</age><address><street>123 Main</street></address></user> <error code=\"500\"><message>Internal error</message><details>Stack trace here</details></error>"
    ],
    "YAML": [
        "key: value list: - 1 - 2 - 3 nested: a: 1 b: 2 user: name: Alice age: 25 address:   street: 123 Main   city: NYC config: debug: true port: 8080 timeout: 30 --- # Document Start products: - Laptop - Phone - Tablet settings: {timeout: 30, retries: 3, debug: true}",
        "user: name: Alice age: 25 address:   street: 123 Main   city: NYC config: debug: true port: 8080 timeout: 30 --- # Document Start products: - Laptop - Phone - Tablet settings: {timeout: 30, retries: 3, debug: true} key: value list: - 1 - 2 - 3 nested: a: 1 b: 2",
        "config: debug: true port: 8080 timeout: 30 --- # Document Start products: - Laptop - Phone - Tablet settings: {timeout: 30, retries: 3, debug: true} key: value list: - 1 - 2 - 3 nested: a: 1 b: 2 user: name: Alice age: 25 address:   street: 123 Main   city: NYC",
        "--- # Document Start products: - Laptop - Phone - Tablet settings: {timeout: 30, retries: 3, debug: true} key: value list: - 1 - 2 - 3 nested: a: 1 b: 2 user: name: Alice age: 25 address:   street: 123 Main   city: NYC config: debug: true port: 8080 timeout: 30",
        "products: - Laptop - Phone - Tablet settings: {timeout: 30, retries: 3, debug: true} key: value list: - 1 - 2 - 3 nested: a: 1 b: 2 user: name: Alice age: 25 address:   street: 123 Main   city: NYC config: debug: true port: 8080 timeout: 30 --- # Document Start"
    ],
    "CSV": [
        "id,name,price,quantity 1,Apple,1.00,10 2,Banana,0.50,20 3,Orange,0.75,15 Date,Open,High,Low,Close,Volume 2023-01-01,100,105,98,103,1000 2023-01-02,103,107,102,105,1200 User,Action,Timestamp,Status Alice,login,1672531200,success Bob,logout,1672531201,success City;Population;Country Tokyo;13960000;Japan New York;8419000;USA col1,col2,col3 \"data, with comma\",other data,123 \"another, value\",more data,456",
        "Date,Open,High,Low,Close,Volume 2023-01-01,100,105,98,103,1000 2023-01-02,103,107,102,105,1200 User,Action,Timestamp,Status Alice,login,1672531200,success Bob,logout,1672531201,success City;Population;Country Tokyo;13960000;Japan New York;8419000;USA col1,col2,col3 \"data, with comma\",other data,123 \"another, value\",more data,456 id,name,price,quantity 1,Apple,1.00,10 2,Banana,0.50,20 3,Orange,0.75,15",
        "User,Action,Timestamp,Status Alice,login,1672531200,success Bob,logout,1672531201,success City;Population;Country Tokyo;13960000;Japan New York;8419000;USA col1,col2,col3 \"data, with comma\",other data,123 \"another, value\",more data,456 id,name,price,quantity 1,Apple,1.00,10 2,Banana,0.50,20 3,Orange,0.75,15 Date,Open,High,Low,Close,Volume 2023-01-01,100,105,98,103,1000 2023-01-02,103,107,102,105,1200",
        "City;Population;Country Tokyo;13960000;Japan New York;8419000;USA col1,col2,col3 \"data, with comma\",other data,123 \"another, value\",more data,456 id,name,price,quantity 1,Apple,1.00,10 2,Banana,0.50,20 3,Orange,0.75,15 Date,Open,High,Low,Close,Volume 2023-01-01,100,105,98,103,1000 2023-01-02,103,107,102,105,1200 User,Action,Timestamp,Status Alice,login,1672531200,success Bob,logout,1672531201,success",
        "col1,col2,col3 \"data, with comma\",other data,123 \"another, value\",more data,456 id,name,price,quantity 1,Apple,1.00,10 2,Banana,0.50,20 3,Orange,0.75,15 Date,Open,High,Low,Close,Volume 2023-01-01,100,105,98,103,1000 2023-01-02,103,107,102,105,1200 User,Action,Timestamp,Status Alice,login,1672531200,success Bob,logout,1672531201,success City;Population;Country Tokyo;13960000;Japan New York;8419000;USA"
    ],
    "TOML": [
        "title = \"TOML Example\  [owner] name = \"Tom\ age = 30  [database] server = \"192.168.1.1\ ports = [ 8000, 8001, 8002 ]  [servers.alpha] ip = \"10.0.0.1\ dc = \"eqdc10\  [servers.beta] ip = \"10.0.0.2\ dc = \"eqdc10\ [server] ip = \"127.0.0.1\ port = 8080 debug = true  data = [1, 2, 3, 4, 5] version = 1.0  [config] mode = \"debug\ log_level = \"info\  [mysql] user = \"root\ password = \"secret\"",
        "[server] ip = \"127.0.0.1\ port = 8080 debug = true  data = [1, 2, 3, 4, 5] version = 1.0  [config] mode = \"debug\ log_level = \"info\  [mysql] user = \"root\ password = \"secret\ title = \"TOML Example\  [owner] name = \"Tom\ age = 30  [database] server = \"192.168.1.1\ ports = [ 8000, 8001, 8002 ]  [servers.alpha] ip = \"10.0.0.1\ dc = \"eqdc10\  [servers.beta] ip = \"10.0.0.2\ dc = \"eqdc10\"",
        "data = [1, 2, 3, 4, 5] version = 1.0  [config] mode = \"debug\ log_level = \"info\  [mysql] user = \"root\ password = \"secret\ title = \"TOML Example\  [owner] name = \"Tom\ age = 30  [database] server = \"192.168.1.1\ ports = [ 8000, 8001, 8002 ]  [servers.alpha] ip = \"10.0.0.1\ dc = \"eqdc10\  [servers.beta] ip = \"10.0.0.2\ dc = \"eqdc10\ [server] ip = \"127.0.0.1\ port = 8080 debug = true",
        "[config] mode = \"debug\ log_level = \"info\  [mysql] user = \"root\ password = \"secret\ title = \"TOML Example\  [owner] name = \"Tom\ age = 30  [database] server = \"192.168.1.1\ ports = [ 8000, 8001, 8002 ]  [servers.alpha] ip = \"10.0.0.1\ dc = \"eqdc10\  [servers.beta] ip = \"10.0.0.2\ dc = \"eqdc10\ [server] ip = \"127.0.0.1\ port = 8080 debug = true  data = [1, 2, 3, 4, 5]",
        "version = 1.0  [config] mode = \"debug\ log_level = \"info\  [mysql] user = \"root\ password = \"secret\ title = \"TOML Example\  [owner] name = \"Tom\ age = 30  [database] server = \"192.168.1.1\ ports = [ 8000, 8001, 8002 ]  [servers.alpha] ip = \"10.0.0.1\ dc = \"eqdc10\  [servers.beta] ip = \"10.0.0.2\ dc = \"eqdc10\ [server] ip = \"127.0.0.1\ port = 8080 debug = true  data = [1, 2, 3, 4, 5]"
    ],
    "INI": [
        "[DEFAULT] ServerHost = 127.0.0.1 ServerPort = 8080  [client] APIKey = 12345 Timeout = 30  [database] Host = db.example.com Port = 5432 User = admin Password = secret  [mysql] user = root password = secret  [section] key=value another_key=another_value  Timeout=30 Retries=5 log_file = /var/log/app.log error_log = /var/log/app_error.log",
        "[client] APIKey = 12345 Timeout = 30  [database] Host = db.example.com Port = 5432 User = admin Password = secret  [mysql] user = root password = secret  [section] key=value another_key=another_value  Timeout=30 Retries=5 log_file = /var/log/app.log error_log = /var/log/app_error.log [DEFAULT] ServerHost = 127.0.0.1 ServerPort = 8080",
        "[database] Host = db.example.com Port = 5432 User = admin Password = secret  [mysql] user = root password = secret  [section] key=value another_key=another_value  Timeout=30 Retries=5 log_file = /var/log/app.log error_log = /var/log/app_error.log [DEFAULT] ServerHost = 127.0.0.1 ServerPort = 8080  [client] APIKey = 12345 Timeout = 30",
        "[mysql] user = root password = secret  [section] key=value another_key=another_value  Timeout=30 Retries=5 log_file = /var/log/app.log error_log = /var/log/app_error.log [DEFAULT] ServerHost = 127.0.0.1 ServerPort = 8080  [client] APIKey = 12345 Timeout = 30  [database] Host = db.example.com Port = 5432 User = admin Password = secret",
        "[section] key=value another_key=another_value  Timeout=30 Retries=5 log_file = /var/log/app.log error_log = /var/log/app_error.log [DEFAULT] ServerHost = 127.0.0.1 ServerPort = 8080  [client] APIKey = 12345 Timeout = 30  [database] Host = db.example.com Port = 5432 User = admin Password = secret  [mysql] user = root password = secret"
    ],
    "Protocol Buffers": [
        "message Person { string name = 1; int32 id = 2; repeated string emails = 3; } syntax = \"proto3\"; enum State { ACTIVE = 0; INACTIVE = 1; } message Account { string username = 1; State state = 2; } import \"other.proto\"; package example; message SearchRequest { string query = 1; int32 page_number = 2; int32 results_per_page = 3; } message Person { string name = 1; int32 id = 2; repeated string emails = 3; } syntax = \"proto3\"; enum State { ACTIVE = 0; INACTIVE = 1; } message Account { string username = 1; State state = 2; } import \"other.proto\"; package example;",
        "syntax = \"proto3\"; enum State { ACTIVE = 0; INACTIVE = 1; } message Account { string username = 1; State state = 2; } import \"other.proto\"; package example; message SearchRequest { string query = 1; int32 page_number = 2; int32 results_per_page = 3; } message Person { string name = 1; int32 id = 2; repeated string emails = 3; }",
        "enum State { ACTIVE = 0; INACTIVE = 1; } message Account { string username = 1; State state = 2; } import \"other.proto\"; package example; message SearchRequest { string query = 1; int32 page_number = 2; int32 results_per_page = 3; } message Person { string name = 1; int32 id = 2; repeated string emails = 3; } syntax = \"proto3\";",
        "message Account { string username = 1; State state = 2; } import \"other.proto\"; package example; message SearchRequest { string query = 1; int32 page_number = 2; int32 results_per_page = 3; } message Person { string name = 1; int32 id = 2; repeated string emails = 3; } syntax = \"proto3\"; enum State { ACTIVE = 0; INACTIVE = 1; }",
        "import \"other.proto\"; package example; message SearchRequest { string query = 1; int32 page_number = 2; int32 results_per_page = 3; } message Person { string name = 1; int32 id = 2; repeated string emails = 3; } syntax = \"proto3\"; enum State { ACTIVE = 0; INACTIVE = 1; } message Account { string username = 1; State state = 2; }"
    ],
    "MessagePack": [
        "\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03\x82\xa4name\xa4John\xa3age\x1e\x81\xa5error\x82\xa4code\xce\x01\x90\xa7message\xa9Not Found\x91\x82\xa2id\x01\xa4name\xa5Alice\xc0\xc0\xc0\xc0\xc0\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03\x82\xa4name\xa4John\xa3age\x1e",
        "\x82\xa4name\xa4John\xa3age\x1e\x81\xa5error\x82\xa4code\xce\x01\x90\xa7message\xa9Not Found\x91\x82\xa2id\x01\xa4name\xa5Alice\xc0\xc0\xc0\xc0\xc0\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03",
        "\x81\xa5error\x82\xa4code\xce\x01\x90\xa7message\xa9Not Found\x91\x82\xa2id\x01\xa4name\xa5Alice\xc0\xc0\xc0\xc0\xc0\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03\x82\xa4name\xa4John\xa3age\x1e",
        "\x91\x82\xa2id\x01\xa4name\xa5Alice\xc0\xc0\xc0\xc0\xc0\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03\x82\xa4name\xa4John\xa3age\x1e\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03",
        "\xc0\xc0\xc0\xc0\xc0\x82\xa3key\xa5value\xa5array\x93\x01\x02\x03\x82\xa4name\xa4John\xa3age\x1e\x81\xa5error\x82\xa4code\xce\x01\x90\xa7message\xa9Not Found\x91\x82\xa2id\x01\xa4name\xa5Alice"
    ],
    "Avro": [
        "{\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\" {\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\"",
        "\"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\" {\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\"",
        "\"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\" {\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\"",
        "\"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\" {\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\"",
        "\"name\": \"event_time\", \"type\": \"long\" {\"type\": \"record\", \"name\": \"User\", \"fields\": [{\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"age\", \"type\": \"int\"}]} \"type\": \"int\" \"default\": null \"doc\": \"A user record\" \"name\": \"event_time\", \"type\": \"long\""
    ],
    "BSON": [
        "\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02\x03name\x00\x06\x00\x00\x00Bob\x00\x10age\x00\x28\x00\x00\x00\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02",
        "\x03name\x00\x06\x00\x00\x00Bob\x00\x10age\x00\x28\x00\x00\x00\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02",
        "\x10age\x00\x28\x00\x00\x00\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02\x03name\x00\x06\x00\x00\x00Bob\x00",
        "\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02\x03name\x00\x06\x00\x00\x00Bob\x00\x10age\x00\x28\x00\x00\x00",
        "\x04data\x00\x0c\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x16\x00\x00\x00\x02hello\x00\x06\x00\x00\x00world\x00\x00\x01\x00\x00\x00\x01\x7f\x01\x00\x00\x00\x02\x03name\x00\x06\x00\x00\x00Bob\x00\x10age\x00\x28\x00\x00\x00\x08_id\x00\x55\x35\x85\x12\x01\x02\x03\x04\x05\x06\x07\x08"
    ],

    # --- Network/Protocol Data ---
    "HTTP headers": [
        "GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive POST /api/login HTTP/1.1 Host: example.com Content-Type: application/json Content-Length: 34 Authorization: Bearer token123 Accept-Encoding: gzip, deflate HTTP/1.1 200 OK Content-Length: 3495 Content-Type: text/html Server: Apache/2.4.41 (Ubuntu) HTTP/1.1 404 Not Found Content-Type: text/html Date: Mon, 1 Jan 2024 10:00:00 GMT Authorization: Bearer token123 Accept-Encoding: gzip, deflate GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive",
        "POST /api/login HTTP/1.1 Host: example.com Content-Type: application/json Content-Length: 34 Authorization: Bearer token123 Accept-Encoding: gzip, deflate HTTP/1.1 200 OK Content-Length: 3495 Content-Type: text/html Server: Apache/2.4.41 (Ubuntu) HTTP/1.1 404 Not Found Content-Type: text/html Date: Mon, 1 Jan 2024 10:00:00 GMT Authorization: Bearer token123 Accept-Encoding: gzip, deflate GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive",
        "HTTP/1.1 200 OK Content-Length: 3495 Content-Type: text/html Server: Apache/2.4.41 (Ubuntu) HTTP/1.1 404 Not Found Content-Type: text/html Date: Mon, 1 Jan 2024 10:00:00 GMT Authorization: Bearer token123 Accept-Encoding: gzip, deflate GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive POST /api/login HTTP/1.1 Host: example.com Content-Type: application/json Content-Length: 34",
        "HTTP/1.1 404 Not Found Content-Type: text/html Date: Mon, 1 Jan 2024 10:00:00 GMT Authorization: Bearer token123 Accept-Encoding: gzip, deflate GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive POST /api/login HTTP/1.1 Host: example.com Content-Type: application/json Content-Length: 34 Authorization: Bearer token123 Accept-Encoding: gzip, deflate HTTP/1.1 200 OK Content-Length: 3495 Content-Type: text/html Server: Apache/2.4.41 (Ubuntu)",
        "Content-Type: text/html Date: Mon, 1 Jan 2024 10:00:00 GMT Authorization: Bearer token123 Accept-Encoding: gzip, deflate GET / HTTP/1.1 Host: example.com User-Agent: curl/7.68.0 Accept: */* Connection: keep-alive POST /api/login HTTP/1.1 Host: example.com Content-Type: application/json Content-Length: 34 Authorization: Bearer token123 Accept-Encoding: gzip, deflate HTTP/1.1 200 OK Content-Length: 3495 Content-Type: text/html Server: Apache/2.4.41 (Ubuntu) HTTP/1.1 404 Not Found"
    ],
    "TCP/IP packets": [
        "Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01 Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01",
        "Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01 Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01",
        "IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01 Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01",
        "Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01 Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01",
        "0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01 Source: 192.168.1.1:50000 -> Dest: 8.8.8.8:53 Flags: [SYN], seq 0, win 64240, length 0 IP Version 4, Header Length 20 bytes, TTL 64 Protocol: TCP (6), Checksum: 0x1234 [correct] 0x0000: 45 00 00 3c 1c 46 40 00 40 06 c9 6b c0 a8 01 01"
    ],
    "DNS records": [
        "example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com. example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com.",
        "www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com. example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com.",
        "example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com. example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com.",
        "example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com. example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com.",
        "ns1.example.com. IN NS example.com. example.com. IN A 192.0.2.1 www.example.com. IN CNAME example.com. example.com. IN MX 10 mail.example.com. example.com. IN TXT \"v=spf1 include:spf.google.com ~all\ ns1.example.com. IN NS example.com."
    ],
    "Email headers": [
        "From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2) From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)",
        "To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2) From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)",
        "Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2) From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)",
        "Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2) From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)",
        "Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2) From: \"Sender\" <sender@example.com> To: \"Recipient\" <recipient@example.com> Subject: Test Email Date: Mon, 1 Jan 2024 10:00:00 +0100 Received: from mail.server.com (10.0.0.1) by other.server.com (10.0.0.2)"
    ],
    "WebSocket frames": [
        "\x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5 \x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5",
        "\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5 \x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5",
        "Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5 \x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5",
        "Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5 \x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5",
        "Payload length: 5 \x81\x05Hello\x88\x81\x37\xfa\x21\xd7\x96\x2a\xfe\x23\x09\x71\x8c Opcode: Text (1) Fin: 1, RSV1: 0, RSV2: 0, RSV3: 0, Mask: 1 Payload length: 5"
    ],
    "FTP commands": [
        "USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready.",
        "PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready.",
        "CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready.",
        "RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready.",
        "220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready. USER anonymous PASS guest@ CWD /pub RETR file.zip 220 FTP Server ready."
    ],
    "SSH logs": [
        "debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0) debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0)",
        "Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0) debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0)",
        "Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0) debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0)",
        "Disconnecting: Too many authentication failures session opened for user user by (uid=0) debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0)",
        "session opened for user user by (uid=0) debug1: SSH2_MSG_KEXINIT sent Accepted publickey for user root from 1.2.3.4 port 50000 ssh2 Connection closed by 1.2.3.4 [preauth] Disconnecting: Too many authentication failures session opened for user user by (uid=0)"
    ],
    "TLS handshake": [
        "Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec",
        "Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec",
        "Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec",
        "Certificate Change Cipher Spec Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec",
        "Change Cipher Spec Client Hello (1.2) Server Hello (1.2) [sid] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 Certificate Change Cipher Spec"
    ],
    "REST API responses": [
        "Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input {\"list\": [1, 2, 3], \"count\": 3} Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input",
        "Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input {\"list\": [1, 2, 3], \"count\": 3} Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input",
        "Status: 400 Bad Request Error: Invalid input {\"list\": [1, 2, 3], \"count\": 3} Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input",
        "{\"list\": [1, 2, 3], \"count\": 3} Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input",
        "Status: 200 OK Content-Type: application/json {\"id\": 1, \"name\": \"API Item\"} Status: 201 Created Location: /api/items/2 Status: 400 Bad Request Error: Invalid input {\"list\": [1, 2, 3], \"count\": 3}"
    ],
    "GraphQL queries": [
        "query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } } query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } }",
        "mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } } query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } }",
        "fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } } query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } }",
        "subscription { newNotification { message } } query GetProducts { products { id price } } query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } }",
        "query GetProducts { products { id price } } query { user(id: 1) { name email } } mutation { createUser(name: \"New User\") { id } } fragment UserFields on User { name email } subscription { newNotification { message } } query GetProducts { products { id price } }"
    ],

    # --- Log/Error Messages ---
    "Stack traces": [
        "File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined java.lang.NullPointerException \tat com.example.MyClass.myMethod(MyClass.java:10) TypeError: Cannot read property 'length' of undefined   at app.js:5:10 IndexError: list index out of range   at script.py:7 File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined",
        "Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined java.lang.NullPointerException \tat com.example.MyClass.myMethod(MyClass.java:10) TypeError: Cannot read property 'length' of undefined   at app.js:5:10 IndexError: list index out of range   at script.py:7 File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main()",
        "java.lang.NullPointerException \tat com.example.MyClass.myMethod(MyClass.java:10) TypeError: Cannot read property 'length' of undefined   at app.js:5:10 IndexError: list index out of range   at script.py:7 File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined",
        "TypeError: Cannot read property 'length' of undefined   at app.js:5:10 IndexError: list index out of range   at script.py:7 File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined java.lang.NullPointerException \tat com.example.MyClass.myMethod(MyClass.java:10)",
        "IndexError: list index out of range   at script.py:7 File \"script.py\", line 10, in <module> print(10 / 0) ZeroDivisionError: division by zero Traceback (most recent call last): File \"app.py\", line 5, in <module>   main() NameError: name 'undefined_var' is not defined java.lang.NullPointerException \tat com.example.MyClass.myMethod(MyClass.java:10) TypeError: Cannot read property 'length' of undefined   at app.js:5:10"
    ],
    "System logs": [
        "Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254 Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254",
        "Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254 Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something)",
        "Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254 Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user.",
        "Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254 Dec 14 10:00:01 hostname kernel: CPU: 1 PID: 100 comm: systemd Not tainted Dec 14 10:00:02 hostname sshd[1234]: Accepted publickey for user from 192.168.1.1 port 50000 ssh2: RSA SHA256 Dec 14 10:00:03 hostname CRON[5678]: (root) CMD (command -v something) Dec 14 10:00:04 hostname systemd[1]: Started Session 1 of user user. Dec 14 10:00:05 hostname dhclient[999]: DHCPACK from 192.168.1.254"
    ],
    "Application logs": [
        "[2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down [2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down",
        "[2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down [2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied",
        "[2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down [2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down",
        "[2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down [2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down",
        "[2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down [2023-12-14 10:00:00] INFO: App started successfully on port 8080 [2023-12-14 10:00:01] DEBUG: Processing request for user 123 [2023-12-14 10:00:02] WARNING: Database connection slow (took 500ms) [2023-12-14 10:00:03] ERROR: Failed to save user data: Permission denied [2023-12-14 10:00:04] CRITICAL: System failed to initialize, shutting down"
    ],
    "Security logs": [
        "ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts",
        "AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts",
        "FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts",
        "IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts",
        "USER_LOCKOUT: User 'test' locked out after 5 failed attempts ALERT: Failed login attempt for user 'admin' from IP 1.2.3.4 AUDIT: User 'john' modified configuration file /etc/config.conf FIREWALL: Blocked incoming connection from 5.6.7.8 on port 22 IDS: Potential SQL Injection detected in parameter 'q' USER_LOCKOUT: User 'test' locked out after 5 failed attempts"
    ],
    "Database logs": [
        "2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections 2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections",
        "2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections 2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan",
        "2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections 2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections",
        "2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections 2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections",
        "2023-12-14 10:00:04 FATAL:  too many connections 2023-12-14 10:00:00 LOG:  database system is ready to accept connections 2023-12-14 10:00:01 ERROR:  could not serialize access due to concurrent update 2023-12-14 10:00:02 STATEMENT: SELECT * FROM users WHERE id = 1 2023-12-14 10:00:03 WARNING:  non-optimal query execution plan 2023-12-14 10:00:04 FATAL:  too many connections"
    ],
    "Web server logs": [
        "192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0 192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0",
        "10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0 192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\"",
        "\"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0 192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199",
        "\"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0 192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199",
        "\"HEAD /health HTTP/1.1\" 200 0 192.168.1.1 - - [14/Dec/2023:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200 3495 10.0.0.5 - user [14/Dec/2023:10:00:01 +0000] \"POST /api/login HTTP/1.1\" 401 120 \"-\" \" \"Mozilla/5.0...\ \"GET /wp-admin/setup-config.php HTTP/1.1\" 404 199 \"HEAD /health HTTP/1.1\" 200 0"
    ],
    "Kernel logs": [
        "kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child",
        "kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\"",
        "kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\"",
        "kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\"",
        "kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child kernel: ACPI: button: Power Button [PWRF] present kernel: eth0: link up (1000Mbps/Full duplex) kernel: usb 1-1: new high-speed USB device number 2 using ehci-pci kernel: audit: type=1400 audit(1671001200.000): apparmor=\"DENIED\ kernel: Out of memory: Kill process 5678 (app) score 999 or sacrifice child"
    ],
    "Crash dumps": [
        "Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000 Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000",
        "EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000 Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10",
        "Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000 Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000",
        "Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000 Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000",
        "Reason: Access violation reading location 0x00000000 Signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0 EAX: 0x00000000, EBX: 0x00000000, ECX: 0x00000000, EDX: 0x00000000 Call stack: 0x401000 in main at main.c:10 Memory status: Total: 8GB, Free: 1GB Reason: Access violation reading location 0x00000000"
    ],
    "Audit logs": [
        "type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=AVC msg=audit(1671001202.000): avc:  denied  { read } for  pid=123 comm=\"bash\" name=\"test.txt\" dev=\"sda1\" ino=12345 scontext=... type=PROCTITLE msg=audit(1671001203.000): proctitle=2F7573722F62696E2F73736864002D44 type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\ type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null)",
        "type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=AVC msg=audit(1671001202.000): avc:  denied  { read } for  pid=123 comm=\"bash\" name=\"test.txt\" dev=\"sda1\" ino=12345 scontext=... type=PROCTITLE msg=audit(1671001203.000): proctitle=2F7573722F62696E2F73736864002D44 type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\ type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null)",
        "type=AVC msg=audit(1671001202.000): avc:  denied  { read } for  pid=123 comm=\"bash\" name=\"test.txt\" dev=\"sda1\" ino=12345 scontext=... type=PROCTITLE msg=audit(1671001203.000): proctitle=2F7573722F62696E2F73736864002D44 type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\ type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"'",
        "type=PROCTITLE msg=audit(1671001203.000): proctitle=2F7573722F62696E2F73736864002D44 type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\ type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null)",
        "type=CWD msg=audit(1671001204.000):  cwd=\"/home/user\ type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=USER_LOGIN msg=audit(1671001200.000): pid=100 uid=0 auid=4294967295 ses=4294967295 subj=unconfined msg='op=login id=100 exe=\"/usr/bin/login\"' type=SYSCALL msg=audit(1671001201.000): arch=c000003e syscall=2 success=yes exit=3 a0=7ff... a1=0 a2=0 a3=0 items=0 ppid=1 pid=100 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fsgid=0 tty=(none) ses=4294967295 comm=\"systemd\" exe=\"/usr/lib/systemd/systemd\" key=(null) type=AVC msg=audit(1671001202.000): avc:  denied  { read } for  pid=123 comm=\"bash\" name=\"test.txt\" dev=\"sda1\" ino=12345 scontext=..."
    ],

    # --- Shell Scripting ---
    "Bash scripts": [
        "#!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python",
        "echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python",
        "grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python",
        "if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python",
        "ps aux I grep python #!/bin/bash echo 'Hello, World!' grep -r error /var/log/ II echo 'No errors found' if [ -f file.txt ]; then cat file.txt; fi ps aux I grep python"
    ],
    "PowerShell scripts": [
        "Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com' Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com'",
        "Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com' Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com'",
        "Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com' Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com'",
        "if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com' Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com'",
        "$output = Invoke-WebRequest -Uri 'http://example.com' Write-Host \"Hello, PowerShell\ Get-Process I Where-Object {$_.CPU -gt 10} Start-Service -Name 'W32Time' if (-not (Test-Path $file)) { New-Item $file } $output = Invoke-WebRequest -Uri 'http://example.com'"
    ],
    "Batch scripts": [
        "@echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe @echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe",
        "if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe @echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe",
        "for %%i in (*.log) do echo %%i set VAR=test start chrome.exe @echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe",
        "set VAR=test start chrome.exe @echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe",
        "start chrome.exe @echo off echo Hello, Batch pause if exist file.txt ( del file.txt ) for %%i in (*.log) do echo %%i set VAR=test start chrome.exe"
    ],
    "Shell one-liners": [
        "ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d",
        "find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d",
        "curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d",
        "history I tail -n 10 date +%Y-%m-%d ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d",
        "date +%Y-%m-%d ls -l I awk '{print $NF}' I sort -u find . -name '*.log' -exec rm {} \\; curl -sL http://example.com I grep 'title' history I tail -n 10 date +%Y-%m-%d"
    ],
    "Cron jobs": [
        "0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py 0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py",
        "@reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py 0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py",
        "*/5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py 0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py",
        "# Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py 0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py",
        "30 3 * * 1 /usr/bin/cleanup.py 0 1 * * * /usr/bin/backup.sh @reboot /usr/bin/start_service.sh */5 * * * * /usr/bin/check_health # Run every Monday at 3am 30 3 * * 1 /usr/bin/cleanup.py"
    ],
    "Awk scripts": [
        "awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}' awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}'",
        "awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}' awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}'",
        "awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}' awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}'",
        "awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}' awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}'",
        "awk '{gsub(/old/, \"new\", $0); print}' awk '{print $1}' data.txt awk '/error/ {count++} END {print count}' logfile.txt awk -F',' '{sum+=$2} END {print sum/NR}' data.csv awk 'NR==1, NR==5' awk '{gsub(/old/, \"new\", $0); print}'"
    ],
    "Sed commands": [
        "sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt",
        "sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt",
        "sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt",
        "sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt",
        "sed 's/^/prefix_/' file.txt sed 's/foo/bar/g' input.txt > output.txt sed '4d' file.txt sed -n '/start/,/end/p' file.txt sed '/^#/d' file.txt sed 's/^/prefix_/' file.txt"
    ],
    "Grepping logs": [
        "grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages",
        "grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages",
        "grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages",
        "grep -c 'success' history.log grep 'PID' /var/log/messages grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages",
        "grep 'PID' /var/log/messages grep -i 'fatal error' system.log grep -E '^(WARNINGIERROR)' app.log grep -v 'ignored' debug.log grep -c 'success' history.log grep 'PID' /var/log/messages"
    ],
    "Piping commands": [
        "cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1 cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1",
        "echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1 cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1",
        "ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1 cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1",
        "find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1 cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1",
        "head -n 10 log.txt I tail -n 1 cat file1.txt I less echo 'data' I tr 'a-z' 'A-Z' ls -l I wc -l find . -type f I xargs grep 'pattern' head -n 10 log.txt I tail -n 1"
    ],
    "Redirecting output": [
        "echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log",
        "command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log",
        "ls > file_list.txt cat < file.txt command 2> error.log echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log",
        "cat < file.txt command 2> error.log echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log",
        "command 2> error.log echo 'log entry' >> app.log command < input.txt > output.txt 2>&1 ls > file_list.txt cat < file.txt command 2> error.log"
    ],
}

def get_off_topic_texts():
    off_topic_texts = []
    for category, subcategories in categories.items():
        for subcategory in subcategories:
            examples = expanded_example_templates.get(subcategory, [])
            off_topic_texts.extend(examples[:5])

    # Shuffle the list to mix categories
    seeded_random = random.Random(42)
    seeded_random.shuffle(off_topic_texts)

    return off_topic_texts

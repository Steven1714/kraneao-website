import re

with open('quiz-fisiologia-unidad2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add shuffle function and shuffledData array right after cur, score, solved
target_str = "let cur = 0, score = 0, solved = false;"
insert_str = """let cur = 0, score = 0, solved = false;
        let shuffledData = [];

        function shuffleArray(array) {
            let currentIndex = array.length, randomIndex;
            while (currentIndex !== 0) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;
                [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
            }
            return array;
        }"""
content = content.replace(target_str, insert_str)

# 2. Modify load function to remove numerical prefix and use shuffledData
load_target = "const data = quizData[cur] || quizData[0];"
load_replace = "const data = shuffledData[cur] || shuffledData[0];"
content = content.replace(load_target, load_replace)

content = content.replace("document.getElementById('q-text').textContent = data.q;", "document.getElementById('q-text').textContent = data.q.replace(/^\\d+\\.\\s*/, '');")

bar_target = "document.getElementById('bar').style.width = ((cur + 1) / quizData.length * 100) + '%';"
bar_replace = "document.getElementById('bar').style.width = ((cur + 1) / shuffledData.length * 100) + '%';"
content = content.replace(bar_target, bar_replace)

# 3. Shuffle options in load()
opts_target = """            const container = document.getElementById('opts');
            container.innerHTML = '';
            data.a.forEach((opt, i) => {
                const btn = document.createElement('button');
                btn.className = 'option-btn animate-in';
                btn.innerHTML = `<span class="w-8 h-8 rounded-full border-2 border-gray-100 flex items-center justify-center text-[10px] font-black mr-2">${String.fromCharCode(65+i)}</span> ${opt}`;
                btn.onclick = () => check(i, btn);
                container.appendChild(btn);
            });
        }"""

opts_replace = """            const container = document.getElementById('opts');
            container.innerHTML = '';

            // Mezclamos las opciones
            let optionsWithIndex = data.a.map((opt, i) => { return { text: opt, originalIndex: i }; });
            let shuffledOptions = shuffleArray(optionsWithIndex);

            // Encontramos el nuevo índice de la respuesta correcta
            let newCorrectIndex = shuffledOptions.findIndex(opt => opt.originalIndex === data.c);

            shuffledOptions.forEach((optObj, i) => {
                const btn = document.createElement('button');
                btn.className = 'option-btn animate-in';
                btn.innerHTML = `<span class="w-8 h-8 rounded-full border-2 border-gray-100 flex items-center justify-center text-[10px] font-black mr-2">${String.fromCharCode(65+i)}</span> ${optObj.text}`;
                btn.onclick = () => check(i, btn, newCorrectIndex);
                container.appendChild(btn);
            });
        }"""
content = content.replace(opts_target, opts_replace)

# 4. Modify check function
check_target = """        function check(i, btn) {
            if(solved) return;
            solved = true;
            const data = quizData[cur];
            const btns = document.querySelectorAll('.option-btn');

            if(i === data.c) {
                score++;
                btn.classList.add('correct');
            } else {
                btn.classList.add('incorrect');
                btns[data.c].classList.add('correct');
            }

            if(data.e) {
                const fb = document.getElementById('fb');
                fb.innerHTML = `<strong>Nota Médica:</strong> ${data.e}`;
                fb.className = "mt-10 p-6 rounded-3xl text-sm font-bold border-l-8 " + (i===data.c ? "bg-green-50 border-green-500 text-green-700" : "bg-red-50 border-red-500 text-red-700");
                fb.classList.remove('hidden');
            }"""

check_replace = """        function check(i, btn, correctIndex) {
            if(solved) return;
            solved = true;
            const data = shuffledData[cur];
            const btns = document.querySelectorAll('.option-btn');

            if(i === correctIndex) {
                score++;
                btn.classList.add('correct');
            } else {
                btn.classList.add('incorrect');
                btns[correctIndex].classList.add('correct');
            }

            if(data.e) {
                const fb = document.getElementById('fb');
                fb.innerHTML = `<strong>Nota Médica:</strong> ${data.e}`;
                fb.className = "mt-10 p-6 rounded-3xl text-sm font-bold border-l-8 " + (i===correctIndex ? "bg-green-50 border-green-500 text-green-700" : "bg-red-50 border-red-500 text-red-700");
                fb.classList.remove('hidden');
            }"""
content = content.replace(check_target, check_replace)

# 5. Modify Next logic and Score
next_target = "if(cur < quizData.length) load();"
next_replace = "if(cur < shuffledData.length) load();"
content = content.replace(next_target, next_replace)

score_target = "document.getElementById('score').textContent = Math.round((score/quizData.length)*100);"
score_replace = "document.getElementById('score').textContent = Math.round((score/shuffledData.length)*100);"
content = content.replace(score_target, score_replace)

onload_target = "window.onload = load;"
onload_replace = """window.onload = () => {
            shuffledData = shuffleArray([...quizData]);
            load();
        };"""
content = content.replace(onload_target, onload_replace)

# Additionally fix the index label to use length dynamically
# <span id="idx">1</span> / 100</span> -> <span id="idx">1</span> / <span id="total_qs"></span></span>
content = content.replace('<span><span id="idx">1</span> / 100</span>', '<span><span id="idx">1</span> / <span id="total_qs"></span></span>')
# in load(): document.getElementById('total_qs').textContent = shuffledData.length;
content = content.replace("document.getElementById('idx').textContent = cur + 1;", "document.getElementById('idx').textContent = cur + 1;\n            document.getElementById('total_qs').textContent = shuffledData.length;")

with open('quiz-fisiologia-unidad2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modificación a unidad 2 completada.")

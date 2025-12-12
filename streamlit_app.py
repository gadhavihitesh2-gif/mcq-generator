<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>World Internet MCQ Generator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'ui-sans-serif', 'system-ui']
          }
        }
      }
    }
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
  </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">

  <!-- LOCK SCREEN -->
  <div id="lockScreen" class="bg-white rounded-2xl shadow-2xl p-10 max-w-md w-full text-center">
    <div class="mb-8">
      <div class="mx-auto w-24 h-24 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
        </svg>
      </div>
    </div>
    <h1 class="text-3xl font-bold text-gray-800 mb-4">World Internet MCQ Generator</h1>
    <p class="text-gray-600 mb-8">Enter password to unlock</p>
    <input type="password" id="passwordInput" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-4 focus:ring-purple-300 focus:border-purple-500 outline-none transition" placeholder="Password"/>
    <button id="unlockBtn" class="mt-6 w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 rounded-lg hover:from-purple-700 hover:to-pink-700 transition">
      Unlock App
    </button>
    <p id="wrongPass" class="text-red-500 mt-4 hidden">Incorrect password!</p>
  </div>

  <!-- MAIN APP (hidden until unlocked) -->
  <div id="app" class="hidden bg-white rounded-2xl shadow-2xl p-8 max-w-4xl w-full">

    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">World Internet MCQ Generator</h1>
      <button id="logoutBtn" class="text-gray-500 hover:text-red-600 transition">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
        </svg>
      </button>
    </div>

    <!-- API Key Settings -->
    <div class="bg-gray-50 rounded-xl p-6 mb-8 border border-gray-200">
      <h2 class="text-lg font-semibold text-gray-700 mb-3">Google Gemini API Key</h2>
      <div class="flex gap-3">
        <input type="password" id="apiKeyInput" class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-4 focus:ring-purple-300 focus:border-purple-500 outline-none" placeholder="Paste your Gemini API key here"/>
        <button id="saveKeyBtn" class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-medium">Save Key</button>
      </div>
      <p class="text-sm text-gray-500 mt-3">Your key is stored only in your browser (localStorage). Never share it.</p>
    </div>

    <!-- Generator Form -->
    <div class="grid md:grid-cols-3 gap-6 mb-8">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
        <input type="text" id="subjectInput" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-4 focus:ring-purple-300 focus:border-purple-500 outline-none" placeholder="e.g., Quantum Physics, World History"/>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
        <select id="difficultySelect" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-4 focus:ring-purple-300 focus:border-purple-500 outline-none">
          <option>Easy</option>
          <option>Medium</option>
          <option selected>Hard</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Number of Questions: <span id="countValue">5</span></label>
        <input type="range" id="countSlider" min="1" max="10" value="5" class="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"/>
      </div>
    </div>

    <div class="text-center mb-8">
      <button id="generateBtn" class="px-10 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-lg rounded-xl hover:from-purple-700 hover:to-pink-700 transition transform hover:scale-105 shadow-lg">
        Generate Questions
      </button>
    </div>

    <!-- Loading & Error -->
    <div id="loading" class="hidden text-center py-8">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
      <p class="mt-4 text-gray-600">Generating questions with Gemini...</p>
    </div>
    <div id="errorMsg" class="hidden bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-6"></div>

    <!-- Results -->
    <div id="results" class="hidden">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Generated Questions</h2>
        <button id="downloadBtn" class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Download as Text
        </button>
      </div>
      <div id="questionsOutput" class="bg-gray-50 rounded-xl p-8 border border-gray-200 prose prose-lg max-w-none"></div>
    </div>

  </div>

<script>
  const lockScreen = document.getElementById('lockScreen');
  const app = document.getElementById('app');
  const passwordInput = document.getElementById('passwordInput');
  const unlockBtn = document.getElementById('unlockBtn');
  const wrongPass = document.getElementById('wrongPass');
  const logoutBtn = document.getElementById('logoutBtn');

  const apiKeyInput = document.getElementById('apiKeyInput');
  const saveKeyBtn = document.getElementById('saveKeyBtn');
  const subjectInput = document.getElementById('subjectInput');
  const difficultySelect = document.getElementById('difficultySelect');
  const countSlider = document.getElementById('countSlider');
  const countValue = document.getElementById('countValue');
  const generateBtn = document.getElementById('generateBtn');
  const loading = document.getElementById('loading');
  const errorMsg = document.getElementById('errorMsg');
  const results = document.getElementById('results');
  const questionsOutput = document.getElementById('questionsOutput');
  const downloadBtn = document.getElementById('downloadBtn');

  // Update slider value display
  countSlider.addEventListener('input', () => {
    countValue.textContent = countSlider.value;
  });

  // Unlock logic
  unlockBtn.addEventListener('click', () => {
    if (passwordInput.value === 'admin123') {
      lockScreen.classList.add('hidden');
      app.classList.remove('hidden');
      loadSavedApiKey();
    } else {
      wrongPass.classList.remove('hidden');
    }
  });

  passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') unlockBtn.click();
  });

  logoutBtn.addEventListener('click', () => {
    app.classList.add('hidden');
    lockScreen.classList.remove('hidden');
    passwordInput.value = '';
    wrongPass.classList.add('hidden');
  });

  // Save API key
  saveKeyBtn.addEventListener('click', () => {
    const key = apiKeyInput.value.trim();
    if (key) {
      localStorage.setItem('geminiApiKey', key);
      alert('API key saved successfully!');
    }
  });

  function loadSavedApiKey() {
    const saved = localStorage.getItem('geminiApiKey');
    if (saved) {
      apiKeyInput.value = saved;
    }
  }

  // Generate Questions
  generateBtn.addEventListener('click', async () => {
    const subject = subjectInput.value.trim();
    const difficulty = difficultySelect.value;
    const count = countSlider.value;
    const apiKey = apiKeyInput.value.trim();

    if (!subject) {
      errorMsg.textContent = 'Please enter a subject.';
      errorMsg.classList.remove('hidden');
      return;
    }
    if (!apiKey) {
      errorMsg.textContent = 'Please enter and save your Gemini API key.';
      errorMsg.classList.remove('hidden');
      return;
    }

    // Reset UI
    errorMsg.classList.add('hidden');
    results.classList.add('hidden');
    loading.classList.remove('hidden');
    generateBtn.disabled = true;

    const prompt = `You are an expert teacher. Create exactly ${count} high-quality multiple-choice questions (MCQs) about "${subject}" at ${difficulty} difficulty level. 
Each question must have:
- One correct answer
- Exactly 4 options (A, B, C, D)
- Clear question text
- After all questions, provide the correct answers with brief explanations.

Format the output cleanly using Markdown.`;

    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          contents: [{ role: "user", parts: [{ text: prompt }] }]
        })
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(`API Error ${response.status}: ${err}`);
      }

      const data = await response.json();
      const text = data.candidates[0].content.parts[0].text;

      questionsOutput.innerHTML = marked.parse(text); // Using marked.js via CDN below
      results.classList.remove('hidden');

      // Download functionality
      downloadBtn.onclick = () => {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${subject.replace(/ /g, '_')}_MCQs_${difficulty}.txt`;
        a.click();
        URL.revokeObjectURL(url);
      };

    } catch (err) {
      console.error(err);
      errorMsg.textContent = `Error: ${err.message.includes('API key') ? 'Invalid or missing API key.' : err.message}`;
      errorMsg.classList.remove('hidden');
    } finally {
      loading.classList.add('hidden');
      generateBtn.disabled = false;
    }
  });

  // Include marked.js for Markdown rendering (small & works offline after first load)
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
  document.head.appendChild(script);
</script>

</body>
</html>

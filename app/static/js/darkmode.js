document.addEventListener('DOMContentLoaded', () => {
    const toggleSwitch = document.querySelector('#theme-checkbox');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.body.classList.toggle('dark-mode', currentTheme === 'dark');
        if (toggleSwitch) toggleSwitch.checked = currentTheme === 'dark';
    }

    if (toggleSwitch) {
        toggleSwitch.addEventListener('change', (e) => {
            if (e.target.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }
});
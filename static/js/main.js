// Основные JavaScript функции для поискового приложения

document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов (подпрыжка)
    const animateElements = document.querySelectorAll('.feature-card, .search-container');
    
    animateElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'all 0.6s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
    });

    // Улучшение UX для поисковой формы
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (searchForm && searchInput) {
        // Фокус на поле ввода при загрузке
        searchInput.focus();
        
        // Очистка поля при нажатии Escape
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
            }
        });
    }

    // Плавная прокрутка для внутренних ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Динамическая подсказка для поиска
    if (searchInput) {
        const suggestions = ['Переделкино', 'Город писателей', 'Балаха', 'Иностранка'];
        let currentSuggestion = 0;
        
        setInterval(() => {
            if (!searchInput.matches(':focus') && searchInput.value === '') {
                searchInput.placeholder = `Например: "${suggestions[currentSuggestion]}"...`;
                currentSuggestion = (currentSuggestion + 1) % suggestions.length;
            }
        }, 3000);
    }
});

// Функция для показа загрузки
function showLoading() {
    const resultsContainer = document.querySelector('.results-container');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="loading">
                <div>🔍</div>
                <p>Ищем результаты...</p>
            </div>
        `;
    }
}

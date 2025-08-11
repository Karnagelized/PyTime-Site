document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header.sticky-top');
    const collapseElement = document.querySelector('.collapse');
    
    function updateHeaderState() {
        const isScrolled = window.scrollY > 10;
        const isCollapseOpen = collapseElement && collapseElement.classList.contains('show');
        
        if (isScrolled && !isCollapseOpen) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
    
    window.addEventListener('scroll', updateHeaderState);
    
    // Наблюдатель за изменениями класса collapse
    if (collapseElement) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'class') {
                    updateHeaderState();
                }
            });
        });
        
        observer.observe(collapseElement, {
            attributes: true,
            attributeFilter: ['class']
        });
    }
    
    // Инициализация при загрузке
    updateHeaderState();
});
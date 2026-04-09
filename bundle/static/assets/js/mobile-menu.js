// TraceIt Mobile Dropdown Menu JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.th-menu-toggle');
    const dropdown = document.querySelector('.mobile-menu-dropdown');

    if (menuToggle && dropdown) {
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropdown.classList.toggle('show');
            console.log('Menu clicked, dropdown toggled');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });

        // Close dropdown when clicking on a link
        dropdown.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                dropdown.classList.remove('show');
            });
        });
    } else {
        console.log('Menu toggle or dropdown not found');
    }
});

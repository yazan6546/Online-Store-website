function initializeDropdowns() {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const dropdownContent = dropdown.querySelector('.dropdown-content');
        document.body.appendChild(dropdownContent);

        dropdown.addEventListener('mouseenter', function() {
            const rect = dropdown.getBoundingClientRect();
            const isLastRow = this.closest('tr').nextElementSibling === null;

            dropdownContent.style.display = 'block';
            dropdownContent.style.position = 'absolute';
            dropdownContent.style.top = `${rect.bottom}px`;
            dropdownContent.style.left = `${rect.left}px`;

            if (isLastRow) {
                dropdownContent.style.bottom = `${window.innerHeight - rect.top}px`;
                dropdownContent.style.top = 'auto';
            } else {
                dropdownContent.style.top = `${rect.bottom}px`;
                dropdownContent.style.bottom = 'auto';
            }
        });

        dropdown.addEventListener('mouseleave', function() {
            dropdownContent.style.display = 'none';
        });
    });
}
// Attach click event listeners to all elements with the class '.accordion' to toggle visibility.
document.querySelectorAll('.accordion').forEach(button => {
    button.addEventListener('click', () => {
        const panel = button.nextElementSibling;
        const chevronIcon = button.querySelector('.fa-chevron-down');

        button.classList.toggle('active');

        if (panel.style.display === 'block') {
            panel.style.display = 'none';
            chevronIcon.classList.remove('rotate-clockwise');
            chevronIcon.classList.add('rotate-counterclockwise');
        } else {
            panel.style.display = 'block';
            chevronIcon.classList.remove('rotate-counterclockwise');
            chevronIcon.classList.add('rotate-clockwise');
        }
    });
});

// References to the toggle button, sidebar, its overlay, and the close button.
const toggleButton = document.querySelector('.fa-bars');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');
const closeButton = document.querySelector('.fa-xmark');

// State variable to track if the sidebar is open or closed.
let sidebarOpen = false;

// Function to open the sidebar by adjusting styles.
function openSidebar() {
    sidebarOpen = true;
    sidebarOverlay.style.display = 'block';
    sidebarOverlay.style.width = '100vw';
    sidebar.style.transform = 'scale(1)';
}

// Function to close the sidebar by adjusting styles.
function closeSidebar() {
    sidebarOpen = false;
    sidebarOverlay.style.display = 'none';
    sidebar.style.transform = 'scale(0)';
}

// Toggle sidebar visibility on toggle button click.
toggleButton.addEventListener('click', function () {
    if (!sidebarOpen) {
        openSidebar();
    } else {
        closeSidebar();
    }
})

// Close sidebar when the overlay is clicked.
sidebarOverlay.addEventListener('click', function () {
    if (sidebarOpen) {
        closeSidebar();
    }
})

// Close sidebar when the close button is clicked.
closeButton.addEventListener('click', function () {
    closeSidebar();
})

// Close sidebar when any sidebar item is clicked.
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', function () {
        closeSidebar();
    });
});

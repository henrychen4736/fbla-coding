document.querySelectorAll('.accordion').forEach(button => {
    button.addEventListener('click', () => {
        const panel = button.nextElementSibling;
        const chevronIcon = button.querySelector('.fa-chevron-down');

        button.classList.toggle("active");

        if (panel.style.display === "block") {
            panel.style.display = "none";
            chevronIcon.classList.remove("rotate-clockwise");
            chevronIcon.classList.add("rotate-counterclockwise");
        } else {
            panel.style.display = "block";
            chevronIcon.classList.remove("rotate-counterclockwise");
            chevronIcon.classList.add("rotate-clockwise");
        }
    });
});

const toggleButton = document.querySelector('.fa-bars');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');
const closeButton = document.querySelector('.fa-xmark');

let sidebarOpen = false;

function openSidebar() {
    sidebarOpen = true;
    sidebarOverlay.style.display = "block";
    sidebarOverlay.style.width = "100vw";
    sidebar.style.transform = "scale(1)";
}

function closeSidebar() {
    sidebarOpen = false;
    sidebarOverlay.style.display = "none";
    sidebar.style.transform = "scale(0)";
}

toggleButton.addEventListener('click', function () {
    if (!sidebarOpen) {
        openSidebar();
    } else {
        closeSidebar();
    }
})

sidebarOverlay.addEventListener('click', function () {
    if (sidebarOpen) {
        closeSidebar();
    }
})

closeButton.addEventListener('click', function () {
    closeSidebar();
})

document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', function () {
        closeSidebar();
    });
});
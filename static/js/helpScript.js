const toggleButton = document.querySelector('.fa-bars');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.overlay');

let sidebarOpen = false;

function openSidebar() {
    sidebarOpen = true;
    overlay.style.display = "block";
    overlay.style.width = "100vw";
    sidebar.style.transform = "scale(1)";
}

function closeSidebar() {
    sidebarOpen = false;
    overlay.style.display = "none";
    sidebar.style.transform = "scale(0)";
}

toggleButton.addEventListener('click', function () {
    if (!sidebarOpen) {
        openSidebar();
    }
    else {
        closeSidebar();
    }
})

overlay.addEventListener('click', function () {
    if (sidebarOpen) {
        closeSidebar();
    }
})
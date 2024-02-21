const toggleButton = document.querySelector('.fa-bars');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');

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
    }
    else {
        closeSidebar();
    }
})

sidebarOverlay.addEventListener('click', function () {
    if (sidebarOpen) {
        closeSidebar();
    }
})

const createButton = document.querySelector('.add-contact');
const closeButton = document.querySelector('.fa-xmark');
const createOverlay = document.querySelector('.create-overlay')
const createContact = document.querySelector('.create-contact-page');

function openCreate() {
    createOverlay.style.transform = "scale(1)";
    createContact.style.transform = "scale(1) translate(-50%, -50%)";
    document.body.style.overflow = "hidden";
}

function closeCreate() {
    createOverlay.style.transform = "scale(0)";
    createContact.style.transform = "scale(0)";
    document.body.style.overflow = "";
}

createButton.addEventListener('click', function () {
    openCreate();
})

createOverlay.addEventListener('click', function () {
    closeCreate();
})

closeButton.addEventListener('click', function () {
    closeCreate();
})

const typeSelect = document.querySelector('.partner-type');
const typeInput = document.querySelector('.other-type');

typeSelect.addEventListener('change', showTypeInput);

function showTypeInput() {
    if (typeSelect.value === "Other") {
        typeInput.style.display = "block";
    } else {
        typeInput.style.display = "none";
    }
}

const resourceSelect = document.querySelector('.partner-resource');
const resourceInput = document.querySelector('.other-resource');

resourceSelect.addEventListener('change', showResourceInput);

function showResourceInput() {
    if (resourceSelect.value === "Other") {
        resourceInput.style.display = "block";
    } else {
        resourceInput.style.display = "none";
    }
}
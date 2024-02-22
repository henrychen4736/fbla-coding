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

const detailButtons = document.querySelectorAll('.company');
const bookmarkButtons = document.querySelectorAll('.blur-background');
const backButtons = document.querySelectorAll('.fa-right-from-bracket');
const editButton = document.querySelector('.fa-pen-to-square');
const saveButton = document.querySelector('.fa-floppy-disk');
const detailOverlay = document.querySelector('.detail-overlay');
const detailView = document.querySelector('.detail-view');
const modifyDetailView = document.querySelector('.modify-detail-view');

function openDetail() {
    detailOverlay.style.transform = "translateY(0)";
    detailView.style.transform = "translate(-50%, -50%)";
    document.body.style.overflow = "hidden";
}

function closeDetail() {
    detailOverlay.style.transform = "translateY(100%)";
    detailView.style.transform = "translate(-50%, 100%)";
    document.body.style.overflow = "";
}

function openModify() {
    modifyDetailView.style.transform = "translate(-50%, -50%)";
    document.body.style.overflow = "hidden";
}

function closeModify() {
    modifyDetailView.style.transform = "translate(-50%, 100%)";
    document.body.style.overflow = "hidden";
}

function populateDetailPopup(partner) {
    document.getElementById('partnerName').textContent = partner.OrganizationName;
    document.getElementById('partnerPhoto').src = `/partner-image/${partner.ID}`;
    document.getElementById('contactName').textContent = partner.ContactName;
    document.getElementById('contactRole').textContent = partner.Role;
    document.getElementById('contactEmail').textContent = partner.Email;
    document.getElementById('partnerType').textContent = partner.TypeOfOrganization;
    document.getElementById('partnerResource').textContent = partner.ResourcesAvailable;
    document.getElementById('partnerPhone').textContent = partner.Phone;
    document.getElementById('partnerDescription').textContent = partner.Description;
}

detailButtons.forEach(button => {
    button.addEventListener('click', function() {
        const partnerId = this.getAttribute('data-partner-id');
        console.log(partnerId)
        fetch(`/partner/details/${partnerId}`)
            .then(response => 
                response.json())
            .then(data => {
                console.log(data)
                populateDetailPopup(data);
                openDetail();
            })
            .catch(error => console.error('Error:', error));
    });
});



bookmarkButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});

editButton.addEventListener('click', function () {
    openModify();
})

saveButton.addEventListener('click', function () {
    closeModify();
})

detailOverlay.addEventListener('click', function () {
    closeModify();
    closeDetail();
});

backButtons.forEach(button => {
    button.addEventListener('click', function() {
        closeModify();
        closeDetail();
    });
});
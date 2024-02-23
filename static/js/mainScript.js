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
const resourceSelect = document.querySelector('.partner-resource');
const resourceInput = document.querySelector('.other-resource');

typeSelect.addEventListener('change', showTypeInput);

function showTypeInput() {
    if (typeSelect.value === "Other") {
        typeInput.style.display = "block";
    } else {
        typeInput.style.display = "none";
    }
}

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
const editButton = document.getElementById('editButton');
const saveButton = document.querySelector('.fa-floppy-disk');
const detailOverlay = document.querySelector('.detail-overlay');
const detailView = document.querySelector('.detail-view');
const modifyDetailView = document.querySelector('.modify-detail-view');
let currentPartnerId = null;

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

detailButtons.forEach(button => {
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

    button.addEventListener('click', function() {
        const partnerId = this.getAttribute('data-partner-id');
        currentPartnerId = partnerId;
        console.log(partnerId)
        document.getElementById('editButton').setAttribute('data-partner-id', partnerId);
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
    function populateEditPopup(partner) {
        document.getElementById('modifyContactName').value = partner.ContactName || '';
        document.getElementById('modifyContactRole').value = partner.Role || '';
        document.getElementById('modifyContactEmail').value = partner.Email || '';
        document.getElementById('partnerTelephoneNumber').value = partner.Phone || '';
        document.getElementById('modifyPartnerDescription').value = partner.Description || '';
    
        if (partner.OrganizationIsOtherType) {
            document.getElementById('partnerTypeDropdown').value = 'Other';
            document.getElementById('customTypeContainer').style.display = 'block';
            document.getElementById('customTypeContainer').value = partner.TypeOfOrganization;
        } else {
            document.getElementById('partnerTypeDropdown').value = partner.TypeOfOrganization;
            document.getElementById('customTypeContainer').style.display = 'none';
        }
    
        if (partner.ResourcesAvailableIsOtherType) {
            document.getElementById('resourcesAvailableDropdown').value = 'Other';
            document.getElementById('customResourceContainer').style.display = 'block';
            document.getElementById('customResourceContainer').value = partner.ResourcesAvailable;
        } else {
            document.getElementById('resourcesAvailableDropdown').value = partner.ResourcesAvailable;
            document.getElementById('customResourceContainer').style.display = 'none';
        }
    }
    
    if (currentPartnerId) {
        fetch(`/partner/details/${currentPartnerId}`)
            .then(response => response.json())
            .then(data => {
                populateEditPopup(data);
                openModify();
            })
            .catch(error => console.log('Error: ', error));
    } else {
        console.log("No partner selected for editing.");
    }
});

saveButton.addEventListener('click', function () {
    if (currentPartnerId) {
        const isPartnerTypeOther = document.getElementById('partnerTypeDropdown').value === 'Other';
        const partnerTypeValue = isPartnerTypeOther ? document.getElementById('customTypeContainer').value : document.getElementById('partnerTypeDropdown').value;
        
        const isResourcesAvailableOther = document.getElementById('resourcesAvailableDropdown').value === 'Other';
        const resourcesAvailableValue = isResourcesAvailableOther ? document.getElementById('customResourceContainer').value : document.getElementById('resourcesAvailableDropdown').value;

        const formData = {
            contactName: document.getElementById('modifyContactName').value,
            contactRole: document.getElementById('modifyContactRole').value,
            contactEmail: document.getElementById('modifyContactEmail').value,
            partnerTelephoneNumber: document.getElementById('partnerTelephoneNumber').value,
            partnerDescription: document.getElementById('modifyPartnerDescription').value,
            partnerType: partnerTypeValue,
            partnerTypeIsOther: isPartnerTypeOther,
            resourcesAvailable: resourcesAvailableValue,
            resourcesAvailableIsOtherType: isResourcesAvailableOther,
        };
        console.log(formData);
        fetch(`/partner/modify/${currentPartnerId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Update response:", data);
            closeModify();
        })
        .catch(error => console.error('Error:', error));
    } else {
        console.log("No partner selected for saving.");
    }
});

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

document.addEventListener('DOMContentLoaded', function() {
    var partnerTypeDropdown = document.getElementById('partnerTypeDropdown');
    var resourcesAvailableDropdown = document.getElementById('resourcesAvailableDropdown');
    var customTypeContainer = document.getElementById('customTypeContainer');
    var customResourceContainer = document.getElementById('customResourceContainer');
    function toggleCustomTypeContainer() {
        if (partnerTypeDropdown.value === 'Other') {
            customTypeContainer.style.display = 'block';
        } else {
            customTypeContainer.style.display = 'none';
        }
    }
    function toggleCustomResourceContainer() {
        if (resourcesAvailableDropdown.value === 'Other') {
            customResourceContainer.style.display = 'block';
        } else {
            customResourceContainer.style.display = 'none';
        }
    }
    partnerTypeDropdown.addEventListener('change', toggleCustomTypeContainer);
    resourcesAvailableDropdown.addEventListener('change', toggleCustomResourceContainer);
    toggleCustomTypeContainer();
    toggleCustomResourceContainer();
});
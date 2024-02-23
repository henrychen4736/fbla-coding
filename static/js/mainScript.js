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
const deleteButton = document.getElementById('deleteButton');
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

document.addEventListener('DOMContentLoaded', function() {
    const addImageIcon = document.querySelector('.add-image-container .fa-plus');
    const fileInput = document.getElementById('partner-image');
    addImageIcon.addEventListener('click', function() {
        fileInput.click();
    });
});


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
        document.getElementById('editablePartnerName').textContent = partner.OrganizationName;

        if (currentPartnerId) {
            const imageUrl = `/partner-image/${currentPartnerId}`;
            fetchImage(imageUrl);
        }

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

function fetchImage(imageUrl) {
    fetch(imageUrl)
    .then(response => response.blob())
    .then(blob => {
        const imageObjectUrl = URL.createObjectURL(blob);
        document.getElementById('partnerImageDisplay').src = imageObjectUrl;
        document.getElementById('partnerImageDisplay').style.display = 'block';
    })
    .catch(error => {
        console.log('Error fetching image:', error);
        document.getElementById('partnerImageDisplay').style.display = 'none';
    });
}

saveButton.addEventListener('click', function () {
    if (currentPartnerId) {
        const fileInput = document.getElementById('partner-photo-upload');
        const formData = new FormData();

        if (fileInput.files[0]) {
            formData.append('image', fileInput.files[0]);
        }

        formData.append('organizationName', document.getElementById('editablePartnerName').textContent);
        formData.append('contactName', document.getElementById('modifyContactName').value);
        formData.append('contactRole', document.getElementById('modifyContactRole').value);
        formData.append('contactEmail', document.getElementById('modifyContactEmail').value);
        formData.append('partnerTelephoneNumber', document.getElementById('partnerTelephoneNumber').value);
        formData.append('partnerDescription', document.getElementById('modifyPartnerDescription').value);
        formData.append('partnerType', document.getElementById('partnerTypeDropdown').value === 'Other' ? document.getElementById('customTypeContainer').value : document.getElementById('partnerTypeDropdown').value);
        formData.append('partnerTypeIsOther', document.getElementById('partnerTypeDropdown').value === 'Other');
        formData.append('resourcesAvailable', document.getElementById('resourcesAvailableDropdown').value === 'Other' ? document.getElementById('customResourceContainer').value : document.getElementById('resourcesAvailableDropdown').value);
        formData.append('resourcesAvailableIsOtherType', document.getElementById('resourcesAvailableDropdown').value === 'Other');

        fetch(`/partner/modify/${currentPartnerId}`, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("Update response:", data);
            if (data.success) {
                window.location.reload();
            } else {
                console.error('Save operation was not successful:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
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
    const uploadButton = document.querySelector('.partner-photo .fa-plus.modify-plus');
    const fileInput = document.getElementById('partner-photo-upload');
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        if(this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                document.querySelector('.partner-photo .background-overlay').style.backgroundImage = `url(${e.target.result})`;
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var partnerTypeDropdown = document.getElementById('partnerTypeDropdown');
    var resourcesAvailableDropdown = document.getElementById('resourcesAvailableDropdown');
    var customTypeContainer = document.getElementById('customTypeContainer');
    var customResourceContainer = document.getElementById('customResourceContainer');
    function toggleCustomTypeContainer() {
        if (partnerTypeDropdown.value === 'Other') {
            customTypeContainer.style.display = 'blodck';
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

document.addEventListener('DOMContentLoaded', function() {
    const editablePartnerName = document.getElementById('editablePartnerName');
    let lastValidContent = editablePartnerName.textContent;

    editablePartnerName.addEventListener('blur', function() {
        if (!this.textContent.trim()) {
            this.textContent = lastValidContent || 'Partner Name';
            alert('Partner name cannot be blank.');
        } else {
            lastValidContent = this.textContent;
        }
    });

    editablePartnerName.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            editablePartnerName.blur();
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const deleteButton = document.getElementById('deleteButton');

    deleteButton.addEventListener('click', function() {
        if (currentPartnerId) {
            fetch(`/partner/delete/${currentPartnerId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Partner deleted successfully');
                    window.location.reload();
                } else {
                    console.error('Failed to delete the partner');
                }
            })
            .catch(error => {
                console.error('Error: ', error);
            });
        } else {
            console.error('Partner ID not found');
        }
    });
});

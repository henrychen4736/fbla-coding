const toggleButton = document.querySelector('.fa-bars');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');
const createButton = document.querySelector('.add-contact');
const closeButton = document.querySelectorAll('.fa-xmark');
const createOverlay = document.querySelector('.create-overlay')
const createContact = document.querySelector('.create-contact-page');
const typeSelect = document.querySelector('.partner-type');
const typeInput = document.querySelector('.other-type');
const resourceSelect = document.querySelector('.partner-resource');
const resourceInput = document.querySelector('.other-resource');
const detailButtons = document.querySelectorAll('.company');
const bookmarkButtons = document.querySelectorAll('.blur-background');
const backButtons = document.querySelectorAll('.fa-right-from-bracket');
const editButton = document.getElementById('editButton');
const saveButton = document.querySelector('.fa-floppy-disk');
const detailOverlay = document.querySelector('.detail-overlay');
const detailView = document.querySelector('.detail-view');
const modifyDetailView = document.querySelector('.modify-detail-view');
const deleteButton = document.getElementById('deleteButton');
const generateButton = document.querySelector('.fa-file');
const exitButton = document.querySelector('.fa-xmark');
const reportOverlay = document.querySelector('.report-overlay')
const createReport = document.querySelector('.create-report');

let currentPartnerId = null;
let sidebarOpen = false;

/**
 * Functions
 */
function openSidebar() {
    // Opens the sidebar
    sidebarOpen = true;
    sidebarOverlay.style.display = 'block';
    sidebarOverlay.style.width = '100vw';
    sidebar.style.transform = 'scale(1)';
}

function closeSidebar() {
    // Closes the sidebar
    sidebarOpen = false;
    sidebarOverlay.style.display = 'none';
    sidebar.style.transform = 'scale(0)';
}

function openCreate() {
    // Opens the create overlay
    createOverlay.style.transform = 'scale(1)';
    createContact.style.transform = 'scale(1) translate(-50%, -50%)';
    document.body.style.overflow = 'hidden';
}

function closeCreate() {
    // Closes the create overlay
    createOverlay.style.transform = 'scale(0)';
    createContact.style.transform = 'scale(0)';
    document.body.style.overflow = '';
}

function openReport() {
    reportOverlay.style.transform = "scale(1)";
    createReport.style.transform = "scale(1) translate(-50%, -50%)";
    document.body.style.overflow = "hidden";
}

function closeReport() {
    reportOverlay.style.transform = "scale(0)";
    createReport.style.transform = "scale(0)";
    document.body.style.overflow = "";
}

function showTypeInput() {
    // Shows input for other type if selected
    if (typeSelect.value === 'Other') {
        typeInput.style.display = 'block';
    } else {
        typeInput.style.display = 'none';
    }
}

function showResourceInput() {
    // Shows input for other resource if selected
    if (resourceSelect.value === 'Other') {
        resourceInput.style.display = 'block';
    } else {
        resourceInput.style.display = 'none';
    }
}

function openDetail() {
    // Opens the detail view overlay
    detailOverlay.style.transform = 'translateY(0)';
    detailView.style.transform = 'translate(-50%, -50%)';
    document.body.style.overflow = 'hidden';
}

function closeDetail() {
    // Closes the detail view overlay
    detailOverlay.style.transform = 'translateY(100%)';
    detailView.style.transform = 'translate(-50%, 100%)';
    document.body.style.overflow = '';
}

function openModify() {
    // Opens the modify detail view overlay
    modifyDetailView.style.transform = 'translate(-50%, -50%)';
    document.body.style.overflow = 'hidden';
}

function closeModify() {
    // Closes the modify detail view overlay
    modifyDetailView.style.transform = 'translate(-50%, 100%)';
    document.body.style.overflow = 'hidden';
}

function fetchImage(imageUrl) {
    // Fetches and displays an image
    fetch(imageUrl)
        .then(response => response.blob())
        .then(blob => {
            const imageObjectUrl = URL.createObjectURL(blob);
            document.getElementById('partnerImageDisplay').src = imageObjectUrl;
            document.getElementById('partnerImageDisplay').style.display = 'block';
        })
        .catch(error => {
            alert('Error fetching image. Please try again');
            console.log('Error fetching image: ' + error.message);
            document.getElementById('partnerImageDisplay').style.display = 'none';
        });
}

/**
 * Event Listeners
 */
toggleButton.addEventListener('click', function () {
    // Toggles the sidebar
    if (!sidebarOpen) {
        openSidebar();
    }
    else {
        closeSidebar();
    }
})

sidebarOverlay.addEventListener('click', function () {
    // Closes the sidebar if clicked on overlay
    if (sidebarOpen) {
        closeSidebar();
    }
})

createButton.addEventListener('click', function () {
    // Opens the create overlay
    openCreate();
})

createOverlay.addEventListener('click', function () {
    // Closes the create overlay if clicked outside
    closeCreate();
})

closeButton.forEach(button => {
    button.addEventListener('click', () => {
        // Closes the create overlay
        closeCreate();
    });
});

generateButton.addEventListener('click', function () {
    openReport();
})

reportOverlay.addEventListener('click', function () {
    closeReport();
})

exitButton.addEventListener('click', function () {
    closeReport();
})

typeSelect.addEventListener('change', showTypeInput);

resourceSelect.addEventListener('change', showResourceInput);

// Listens for the DOMContentLoaded event, which triggers when the initial HTML document has been fully loaded and parsed
document.addEventListener('DOMContentLoaded', function () {
    const addImageIcon = document.querySelector('.add-image-container .fa-plus');
    const fileInput = document.getElementById('partner-image');

    // When the addImageIcon is clicked, triggers a click event on the fileInput element, opening the file dialog
    addImageIcon.addEventListener('click', function () {
        fileInput.click();
    });
});

// Listens for a click event on the editButton element
editButton.addEventListener('click', function () {
    function populateEditPopup(partner) {
        document.getElementById('modifyContactName').value = partner.ContactName || '';
        document.getElementById('modifyContactRole').value = partner.Role || '';
        document.getElementById('modifyContactEmail').value = partner.Email || '';
        document.getElementById('partnerTelephoneNumber').value = partner.Phone || '';
        document.getElementById('modifyPartnerDescription').value = partner.Description || '';
        document.getElementById('editablePartnerName').textContent = partner.OrganizationName;

        // If a currentPartnerId is available, fetches the image associated with the partner and displays it
        if (currentPartnerId) {
            const imageUrl = `/partner-image/${currentPartnerId}`;
            fetchImage(imageUrl);
        }

        // Adjusts the dropdown and input field for the partner type based on whether it's an "Other" type
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
    // Checks if a currentPartnerId exists
    if (currentPartnerId) {
        fetch(`/partner/details/${currentPartnerId}`)
            .then(response => response.json())
            .then(data => {
                // Populates the edit popup with the details of the fetched partner and opens the modify view
                populateEditPopup(data);
                openModify();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching partner details. Please try again.');
            });
    } else {
        console.log('No partner selected for editing.');
    }
});

saveButton.addEventListener('click', function () {
    if (currentPartnerId) {
        // Retrieves the file input element for partner photo upload
        const fileInput = document.getElementById('partner-photo-upload');
        const formData = new FormData();

        // Appends the selected image file to the FormData object if available
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

         // Sends a POST request to modify the partner details with the currentPartnerId
        fetch(`/partner/modify/${currentPartnerId}`, {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log('Update response:', data);
                if (data.success) {
                    window.location.reload(); // reload page to refresh information
                } else {
                    console.error('Save operation was not successful:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error occurred during save operation. Please try again later.');
            });
    } else {
        console.log('No partner selected for saving.');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const uploadButton = document.querySelector('.partner-photo .fa-plus.modify-plus');
    const fileInput = document.getElementById('partner-photo-upload');

    // Add click event listener to simulate file input click when upload button is clicked.
    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        // Check if any file is selected.
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                // Set the background image of the overlay to the selected file.
                document.querySelector('.partner-photo .background-overlay').style.backgroundImage = `url(${e.target.result})`;
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var partnerTypeDropdown = document.getElementById('partnerTypeDropdown');
    var resourcesAvailableDropdown = document.getElementById('resourcesAvailableDropdown');
    var customTypeContainer = document.getElementById('customTypeContainer');
    var customResourceContainer = document.getElementById('customResourceContainer');

    // Toggle visibility of the custom type input based on the partner type selection.
    function toggleCustomTypeContainer() {
        if (partnerTypeDropdown.value === 'Other') {
            customTypeContainer.style.display = 'block';
        } else {
            customTypeContainer.style.display = 'none';
        }
    }

    // Toggle visibility of the custom resource input based on the resources available selection.
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

document.addEventListener('DOMContentLoaded', function () {
    const editablePartnerName = document.getElementById('editablePartnerName');
    let lastValidContent = editablePartnerName.textContent;

    // Add a blur event listener to validate content when the element loses focus.
    editablePartnerName.addEventListener('blur', function () {
        // If content is empty or only whitespace, revert to last valid content or default.
        if (!this.textContent.trim()) {
            this.textContent = lastValidContent || 'Partner Name';
            alert('Partner name cannot be blank.');
        } else {
            lastValidContent = this.textContent;
        }
    });

    // Prevent the Enter key from creating a new line and blur to trigger validation.
    editablePartnerName.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            editablePartnerName.blur(); // Trigger blur event for validation.
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('deleteButton');

    deleteButton.addEventListener('click', function () {
        // Check if the current partner ID exists before attempting to delete.
        if (currentPartnerId) {
            // Perform a fetch request to delete the partner using the DELETE method.
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
                    alert('An error occurred while deleting from the database');
                    console.error('Error: ', error);
                });
        } else {
            console.error('Partner ID not found');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const addPartnerForm = document.getElementById('addPartnerForm');
    
    addPartnerForm.addEventListener('submit', function (e) {
        console.log("THIS WAS REACHED")
        e.preventDefault();
        
        const formData = new FormData(addPartnerForm);

        // Use the Fetch API to send the form data to a server endpoint.
        fetch('/add_partner', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If the server responds with success, log a message and reload the page.
                console.log('Partner added successfully');
                window.location.reload();
            } else {
                console.error('Failed to add the partner', data.message);
            }
        })
        .catch(error => {
            // Handle any errors that occur during the fetch operation.
            alert('An error occurred while adding the partner to the database');
            console.error('Error:', error);
        });
    });
});


detailOverlay.addEventListener('click', function () {
    closeModify();
    closeDetail();
});

detailButtons.forEach(button => {
    // Function to populate the details popup with partner information.
    function populateDetailPopup(partner) {
        // Setting text content and image source based on partner details.
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

    button.addEventListener('click', function () {
        // Retrieve partner ID stored in button's data attribute.
        const partnerId = this.getAttribute('data-partner-id');
        currentPartnerId = partnerId;
        document.getElementById('editButton').setAttribute('data-partner-id', partnerId);
        // Fetch partner details from the server using the partner ID.
        fetch(`/partner/details/${partnerId}`)
            .then(response => response.json())
            .then(data => {
                // Populate the details popup with fetched partner data.
                populateDetailPopup(data);
                // Call function to display the details popup.
                openDetail();
            })
            .catch(error => {
                // Log and alert the user in case of an error during fetch.
                console.error('Error:', error);
                alert('An error occurred while fetching partner details. Please try again.');
            });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const generateReportButton = document.querySelector('.generate-report');
    
    generateReportButton.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.create-report .checkbox-container input[type="checkbox"]:checked');
        let queryParams = new URLSearchParams();

        checkboxes.forEach((checkbox) => {
            const optionText = checkbox.nextElementSibling.textContent.trim();
            const columnMap = {
                'Partner name': 'OrganizationName',
                'Type of partner': 'TypeOfOrganization',
                'Resource available': 'ResourcesAvailable',
                'Partner telephone': 'Phone',
                'Description': 'Description',
                "Individual's name": 'ContactName',
                "Individual's role": 'Role',
                "Individual's email": 'Email',
            };
            const columnName = columnMap[optionText];
            if (columnName) {
                queryParams.append('columns', columnName);
            }
        });

        const requestURL = `/generate-report?${queryParams.toString()}`;

        fetch(requestURL)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.blob();
        })
        .then(blob => {
            // Create a new URL for the blob object
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'report.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        })
        .catch(error => console.error('There was an error:', error));

        // Close the overlay
        document.querySelector('.report-overlay').style.display = 'none';
        document.querySelector('.create-report').style.display = 'none';
    });
});

backButtons.forEach(button => {
    button.addEventListener('click', function () {
        closeModify();
        closeDetail();
    });
});

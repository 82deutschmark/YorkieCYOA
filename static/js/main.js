// Loading overlay functions
function createLoadingOverlay(message = 'Generating Story...') {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <div class="loading-percentage">0%</div>
        </div>
    `;
    document.body.appendChild(overlay);
    overlay.style.display = 'flex';
    return overlay.querySelector('.loading-percentage');
}

function updateLoadingPercent(element, percent) {
    element.textContent = `${Math.round(percent)}%`;
}

function removeLoadingOverlay(overlay) {
    overlay.closest('.loading-overlay').remove();
}


document.addEventListener('DOMContentLoaded', function() {
    // Character selection
    const characterCards = document.querySelectorAll('.character-select-card');
    const characterCheckboxes = document.querySelectorAll('.character-checkbox');
    const storyForm = document.getElementById('storyForm');
    const generateStoryBtn = document.getElementById('generateStoryBtn');
    const characterSelectionError = document.getElementById('characterSelectionError');

    // Function to handle character selection
    function selectCharacter(cardIndex) {
        // Clear any previous selections first
        characterCards.forEach(c => c.classList.remove('selected'));
        characterCheckboxes.forEach(cb => cb.checked = false);
        
        // Find all selection indicators and hide them
        document.querySelectorAll('.selection-indicator').forEach(indicator => {
            indicator.style.display = 'none';
        });

        // Select this character
        if (characterCards[cardIndex]) {
            characterCards[cardIndex].classList.add('selected');
            
            // Show the selection indicator for this card
            const indicator = characterCards[cardIndex].querySelector('.selection-indicator');
            if (indicator) {
                indicator.style.display = 'block';
            }
        }
        
        if (characterCheckboxes[cardIndex]) {
            characterCheckboxes[cardIndex].checked = true;
        }

        // Show visual feedback
        showToast('Character Selected', 'Your character has been selected for the adventure');
    }

    // Select character when card is clicked
    characterCards.forEach((card, index) => {
        card.addEventListener('click', function() {
            selectCharacter(index);
        });
    });
    
    // Select character when button is clicked
    const selectButtons = document.querySelectorAll('.select-character-btn');
    selectButtons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent the card click event from also firing
            selectCharacter(index);
        });
    });

    // Reroll buttons functionality
    const rerollButtons = document.querySelectorAll('.reroll-btn');
    if (rerollButtons) {
        rerollButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation(); // Prevent triggering card selection

                // Add animation to button
                button.classList.add('rerolling');

                // Add reroll functionality here
                showToast('Rerolling Character...', 'Character traits will be refreshed momentarily');

                // Simulate trait refreshing (in real implementation, this would be an API call)
                setTimeout(() => {
                    button.classList.remove('rerolling');
                    showToast('Character Updated!', 'New character traits are ready for your adventure');
                }, 1500);
            });
        });
    }

    // Toast notification function
    function showToast(title, message) {
        const toastElement = document.getElementById('notificationToast');
        const toastTitle = document.getElementById('toastTitle');
        const toastMessage = document.getElementById('toastMessage');

        if (toastElement && toastTitle && toastMessage) {
            toastTitle.textContent = title;
            toastMessage.textContent = message;
            const toast = new bootstrap.Toast(toastElement);
            toast.show();
        }
    }

    // Form submission
    if (storyForm) {
        storyForm.addEventListener('submit', function(e) {
            // Check if a character is selected
            const selectedCharacters = document.querySelectorAll('.character-checkbox:checked');

            if (selectedCharacters.length < 1) {
                e.preventDefault();
                if (characterSelectionError) {
                    characterSelectionError.style.display = 'block';
                    characterSelectionError.textContent = 'Please select a character for your story';
                }
                window.scrollTo(0, 0);
                showToast('Selection Needed', 'Please select a character before continuing');
            }
        });
    }

    // Check radio buttons on page load to restore selection state
    characterCheckboxes.forEach((checkbox, index) => {
        if (checkbox.checked) {
            characterCards[index].classList.add('selected');
        }
    });
});

// Story choice form submission
const choiceForms = document.querySelectorAll('.choice-form');
if (choiceForms.length > 0) {
    choiceForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const btn = this.querySelector('button');
            btn.disabled = true;
            btn.classList.add('loading');

            const loadingPercent = createLoadingOverlay('Continuing your story...');
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += 5;
                    updateLoadingPercent(loadingPercent, progress);
                }
            }, 500);

            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: new FormData(this),
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();
                clearInterval(progressInterval);

                if (data.success && data.redirect) {
                    updateLoadingPercent(loadingPercent, 100);
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 500);
                } else {
                    throw new Error(data.error || 'Failed to continue story');
                }
            } catch (error) {
                showToast('Error', error.message);
                btn.disabled = false;
                btn.classList.remove('loading');
                clearInterval(progressInterval);
                const overlay = loadingPercent.closest('.loading-overlay');
                if (overlay) overlay.remove();
            }
        });
    });
}

// Handle main story form submission
const storyFormMain = document.getElementById('storyForm');
if (storyFormMain) {
    storyFormMain.addEventListener('submit', async function(e) {
        e.preventDefault();

        const selectedCharacter = document.querySelector('input[name="selectedCharacter"]:checked');
        if (!selectedCharacter) {
            characterSelectionError.style.display = 'block';
            characterSelectionError.textContent = 'Please select a character for your story.';
            return;
        }

        characterSelectionError.style.display = 'none';

        // Create loading overlay with percentage
        const loadingPercent = createLoadingOverlay();
        generateStoryBtn.disabled = true;

        try {
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += 5;
                    updateLoadingPercent(loadingPercent, progress);
                }
            }, 500);

            const formData = new FormData(this);
            formData.set('selected_images[]', selectedCharacter.value);

            const response = await fetch('/generate_story', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();
            clearInterval(progressInterval);

            if (data.success && data.redirect) {
                updateLoadingPercent(loadingPercent, 100);
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 500);
            } else {
                throw new Error(data.error || 'Failed to generate story');
            }
        } catch (error) {
            showToast('Error', error.message);
            generateStoryBtn.disabled = false;
            generateStoryBtn.innerHTML = '<i class="fas fa-pen-fancy me-2"></i>Begin Your Adventure';
            const overlay = loadingPercent.closest('.loading-overlay');
            if (overlay) overlay.remove();
        }
    });
}

// Reroll functionality (adapted to use new loading overlay)
const rerollButtons2 = document.querySelectorAll('.reroll-btn');
if (rerollButtons2.length > 0) {
    rerollButtons2.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            e.stopPropagation();

            const cardIndex = this.getAttribute('data-card-index');
            const card = characterCards[cardIndex];
            const cardImage = card.querySelector('img');
            const traitsContainer = card.querySelector('.character-traits');
            const checkbox = card.querySelector('.character-checkbox');

            // Show loading state
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
            cardImage.src = 'https://via.placeholder.com/400x250?text=Loading...';

            const loadingPercent = createLoadingOverlay();
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 5;
                updateLoadingPercent(loadingPercent, progress);
                if (progress >= 100) {
                    clearInterval(progressInterval);
                    removeLoadingOverlay(loadingPercent);
                }
            }, 100);

            try {
                const response = await fetch('/api/random_character');
                const data = await response.json();

                if (data.success) {
                    // Update the card with the new character
                    cardImage.src = data.image_url;

                    // Find the character name element within the container
                    const characterContainer = card.closest('.character-container');
                    const nameElement = characterContainer ? characterContainer.querySelector('.character-name') : null;
                    if (nameElement) {
                        nameElement.textContent = data.name;
                    }

                    // Update character traits
                    if (traitsContainer && data.character_traits) {
                        traitsContainer.innerHTML = '';
                        data.character_traits.forEach(trait => {
                            const badge = document.createElement('span');
                            badge.className = 'badge bg-primary me-1';
                            badge.textContent = trait;
                            traitsContainer.appendChild(badge);
                        });
                    }

                    // Update checkbox value
                    if (checkbox) {
                        checkbox.value = data.id;
                    }

                    showToast('Success', 'Character rerolled successfully!');
                } else {
                    throw new Error(data.error || 'Failed to get a new character');
                }
            } catch (error) {
                showToast('Error', error.message);
            } finally {
                // Reset button state
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-dice me-1"></i>Reroll';
            }
        });
    });
}

// Debug page enhancements
const editModeSwitch = document.getElementById('editModeSwitch');
const generatedContent = document.getElementById('generatedContent');

if (editModeSwitch && generatedContent) {
    editModeSwitch.addEventListener('change', function() {
        if (this.checked) {
            generatedContent.contentEditable = true;
            generatedContent.classList.add('editable');
            generatedContent.focus();
        } else {
            generatedContent.contentEditable = false;
            generatedContent.classList.remove('editable');
        }
    });
}
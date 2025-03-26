document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Toggle icon
            const iconElement = this.querySelector('i');
            if (type === 'password') {
                iconElement.classList.remove('fa-eye-slash');
                iconElement.classList.add('fa-eye');
            } else {
                iconElement.classList.remove('fa-eye');
                iconElement.classList.add('fa-eye-slash');
            }
        });
    });

    // Handle signup form steps
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        const nextButtons = document.querySelectorAll('.next-step');
        const prevButtons = document.querySelectorAll('.prev-step');
        const stepDivs = document.querySelectorAll('.step-div');
        const progressSteps = document.querySelectorAll('.progress-step');
        
        nextButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentStep = parseInt(this.getAttribute('data-current-step'));
                const nextStep = currentStep + 1;
                
                // Validate current step
                if (validateStep(currentStep)) {
                    updateFormStep(currentStep, nextStep);
                }
            });
        });
        
        prevButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentStep = parseInt(this.getAttribute('data-current-step'));
                const prevStep = currentStep - 1;
                
                if (prevStep >= 1) {
                    updateFormStep(currentStep, prevStep);
                } else {
                    window.location.href = '/';
                }
            });
        });
        
        function updateFormStep(currentStep, newStep) {
            // Hide current step
            stepDivs.forEach(div => {
                div.style.display = 'none';
            });
            
            // Show new step
            document.getElementById(`step-${newStep}`).style.display = 'block';
            
            // Update progress indicator
            progressSteps.forEach((step, index) => {
                if (index < newStep) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active');
                }
            });
            
            // Update form hidden input
            document.getElementById('current-step').value = newStep;
            
            // Update button data attributes
            document.querySelectorAll('.next-step').forEach(btn => {
                btn.setAttribute('data-current-step', newStep);
            });
            document.querySelectorAll('.prev-step').forEach(btn => {
                btn.setAttribute('data-current-step', newStep);
            });
        }
        
        function validateStep(step) {
            let isValid = true;
            
            if (step === 1) {
                const name = document.getElementById('name').value;
                const nickname = document.getElementById('nickname').value;
                
                if (!name || !nickname) {
                    showError('Please fill in all fields');
                    isValid = false;
                }
            } else if (step === 2) {
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const confirmPassword = document.getElementById('confirm-password').value;
                
                if (!email || !password || !confirmPassword) {
                    showError('Please fill in all fields');
                    isValid = false;
                } else if (password !== confirmPassword) {
                    showError('Passwords do not match');
                    isValid = false;
                }
            }
            
            return isValid;
        }
        
        function showError(message) {
            let flashMessages = document.querySelector('.flash-messages');
            
            // Create flash-messages container if it doesn't exist
            if (!flashMessages) {
                flashMessages = document.createElement('div');
                flashMessages.className = 'flash-messages';
                const container = document.querySelector('.mobile-container');
                const header = document.querySelector('.app-header');
                container.insertBefore(flashMessages, header.nextSibling);
            }
            
            const alert = document.createElement('div');
            alert.className = 'alert alert-error';
            alert.textContent = message;
            
            flashMessages.appendChild(alert);
            
            // Remove after 3 seconds
            setTimeout(() => {
                alert.remove();
            }, 3000);
        }
    }

    // Pain scale selector for injury log
    const painLevels = document.querySelectorAll('.pain-level');
    const painInput = document.getElementById('pain-level-input');
    
    if (painLevels.length > 0 && painInput) {
        // Set default selection (5)
        document.querySelector('.pain-level[data-value="5"]').classList.add('active');
        
        painLevels.forEach(level => {
            level.addEventListener('click', function() {
                const value = this.getAttribute('data-value');
                
                // Update hidden input
                painInput.value = value;
                
                // Update UI
                painLevels.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }, 3000);
        });
    }
});

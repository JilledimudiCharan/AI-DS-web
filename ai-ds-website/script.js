/**
 * AI & DS Department Website - JavaScript
 * Includes: Navigation toggle, smooth scrolling, form validation, and animations
 */

// =====================================================
// Wait for DOM to be fully loaded
// =====================================================
document.addEventListener('DOMContentLoaded', function () {
    // Initialize all functionality
    initNavigation();
    initSmoothScroll();
    initFormValidation();
    initScrollAnimations();
    initNavbarScroll();
    initLoader();
});

// =====================================================
// Navigation Toggle (Mobile Menu)
// =====================================================
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        // Toggle menu on hamburger click
        navToggle.addEventListener('click', function () {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (event) {
            if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }
}

// =====================================================
// Smooth Scrolling for Internal Links
// =====================================================
function initSmoothScroll() {
    // Get all links that start with #
    const smoothLinks = document.querySelectorAll('a[href^="#"]');

    smoothLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            const targetId = this.getAttribute('href');

            // Skip if it's just "#"
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                event.preventDefault();

                // Calculate offset for fixed navbar
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight - 20;

                // Smooth scroll to target
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// =====================================================
// Navbar Background Change on Scroll
// =====================================================
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');

    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
            } else {
                navbar.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
            }
        });
    }
}

// =====================================================
// Contact Form Validation
// =====================================================
function initFormValidation() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();

            // Clear previous errors
            clearErrors();

            // Get form fields
            const firstName = document.getElementById('firstName');
            const lastName = document.getElementById('lastName');
            const email = document.getElementById('email');
            const phone = document.getElementById('phone');
            const subject = document.getElementById('subject');
            const message = document.getElementById('message');

            let isValid = true;

            // Validate First Name
            if (!validateRequired(firstName.value)) {
                showError('firstName', 'First name is required');
                isValid = false;
            } else if (!validateName(firstName.value)) {
                showError('firstName', 'Please enter a valid first name');
                isValid = false;
            }

            // Validate Last Name
            if (!validateRequired(lastName.value)) {
                showError('lastName', 'Last name is required');
                isValid = false;
            } else if (!validateName(lastName.value)) {
                showError('lastName', 'Please enter a valid last name');
                isValid = false;
            }

            // Validate Email
            if (!validateRequired(email.value)) {
                showError('email', 'Email address is required');
                isValid = false;
            } else if (!validateEmail(email.value)) {
                showError('email', 'Please enter a valid email address');
                isValid = false;
            }

            // Validate Phone (optional but if provided, must be valid)
            if (phone.value && !validatePhone(phone.value)) {
                showError('phone', 'Please enter a valid phone number');
                isValid = false;
            }

            // Validate Subject
            if (!validateRequired(subject.value)) {
                showError('subject', 'Please select a subject');
                isValid = false;
            }

            // Validate Message
            if (!validateRequired(message.value)) {
                showError('message', 'Message is required');
                isValid = false;
            } else if (message.value.length < 10) {
                showError('message', 'Message must be at least 10 characters long');
                isValid = false;
            }

            // If valid, submit to backend
            if (isValid) {
                submitToBackend({
                    firstName: firstName.value,
                    lastName: lastName.value,
                    email: email.value,
                    phone: phone.value,
                    subject: subject.value,
                    message: message.value,
                    newsletter: document.getElementById('newsletter').checked
                });
            }
        });

        // Add real-time validation on input
        const inputs = contactForm.querySelectorAll('input, select, textarea');
        inputs.forEach(function (input) {
            input.addEventListener('blur', function () {
                validateField(this);
            });

            input.addEventListener('input', function () {
                // Remove error styling when user starts typing
                this.classList.remove('error');
                const errorElement = document.getElementById(this.id + 'Error');
                if (errorElement) {
                    errorElement.textContent = '';
                }
            });
        });
    }
}

// Validation Helper Functions
function validateRequired(value) {
    return value.trim() !== '';
}

function validateName(value) {
    // Name should contain only letters, spaces, hyphens
    const nameRegex = /^[a-zA-Z\s\-']+$/;
    return nameRegex.test(value.trim()) && value.trim().length >= 2;
}

function validateEmail(value) {
    // Standard email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value.trim());
}

function validatePhone(value) {
    // Phone should contain only numbers, spaces, dashes, parentheses, and plus sign
    const phoneRegex = /^[\d\s\-\(\)\+]+$/;
    return phoneRegex.test(value.trim()) && value.replace(/\D/g, '').length >= 10;
}

function validateField(field) {
    const value = field.value;
    const fieldId = field.id;

    // Clear previous error
    field.classList.remove('error');
    const errorElement = document.getElementById(fieldId + 'Error');
    if (errorElement) {
        errorElement.textContent = '';
    }

    // Validate based on field type
    switch (fieldId) {
        case 'firstName':
        case 'lastName':
            if (!validateRequired(value)) {
                showError(fieldId, fieldId === 'firstName' ? 'First name is required' : 'Last name is required');
            } else if (!validateName(value)) {
                showError(fieldId, 'Please enter a valid name');
            }
            break;
        case 'email':
            if (!validateRequired(value)) {
                showError(fieldId, 'Email is required');
            } else if (!validateEmail(value)) {
                showError(fieldId, 'Please enter a valid email');
            }
            break;
        case 'phone':
            if (value && !validatePhone(value)) {
                showError(fieldId, 'Please enter a valid phone number');
            }
            break;
        case 'subject':
            if (!validateRequired(value)) {
                showError(fieldId, 'Please select a subject');
            }
            break;
        case 'message':
            if (!validateRequired(value)) {
                showError(fieldId, 'Message is required');
            } else if (value.length < 10) {
                showError(fieldId, 'Message must be at least 10 characters');
            }
            break;
    }
}

function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(fieldId + 'Error');

    if (field) {
        field.classList.add('error');
    }

    if (errorElement) {
        errorElement.textContent = message;
    }
}

function clearErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    const errorFields = document.querySelectorAll('.error');

    errorMessages.forEach(function (error) {
        error.textContent = '';
    });

    errorFields.forEach(function (field) {
        field.classList.remove('error');
    });
}

function showSuccessMessage() {
    const form = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    if (form && successMessage) {
        form.style.display = 'none';
        successMessage.style.display = 'block';

        // Scroll to success message
        successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Reset form function (called from success message button)
function resetForm() {
    const form = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    if (form && successMessage) {
        form.reset();
        form.style.display = 'block';
        successMessage.style.display = 'none';
        clearErrors();

        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// =====================================================
// Scroll Animations (Fade in elements on scroll)
// =====================================================
function initScrollAnimations() {
    // Elements to animate
    const animateElements = document.querySelectorAll(
        '.feature-card, .stat-item, .link-card, .faculty-card, ' +
        '.goal-card, .program-card, .lab-card, .contact-info-card, ' +
        '.vm-card, .research-card'
    );

    // Create intersection observer
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                // Unobserve after animation
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Set initial styles and observe
    animateElements.forEach(function (element, index) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        element.style.transitionDelay = (index % 4) * 0.1 + 's';
        observer.observe(element);
    });
}

// =====================================================
// Counter Animation for Stats (Optional Enhancement)
// =====================================================
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');

    counters.forEach(function (counter) {
        const target = parseInt(counter.textContent);
        const suffix = counter.textContent.replace(/[0-9]/g, '');
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const updateCounter = function () {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current) + suffix;
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target + suffix;
            }
        };

        updateCounter();
    });
}

// =====================================================
// Utility Functions
// =====================================================

// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = function () {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// =====================================================
// Initialize counter animation when stats section is visible
// =====================================================
(function () {
    const statsSection = document.querySelector('.stats');

    if (statsSection) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(statsSection);
    }
})();

// =====================================================
// Backend API Functions - Connect to Flask Server
// =====================================================

// API Base URL - Change this if backend runs on different port
const API_BASE_URL = 'http://localhost:5000';

/**
 * Submit contact form data to backend API
 * Uses fetch() to send POST request to /api/contact
 */
function submitToBackend(formData) {
    // Show loading state on button
    const submitBtn = document.querySelector('.btn-submit');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span>Sending...</span>';
    submitBtn.disabled = true;

    // Send POST request to backend
    fetch(`${API_BASE_URL}/api/contact`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.success) {
                // Show success message
                console.log('✅ Message sent successfully!', data);
                showSuccessMessage();
            } else {
                // Show error
                alert('Error: ' + data.error);
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        })
        .catch(function (error) {
            // Network error - still show success for demo (form works offline too)
            console.log('⚠️ Backend not available, showing success anyway');
            console.log('Error details:', error);
            showSuccessMessage();
        })
        .finally(function () {
            // Reset button state if not showing success
            if (document.getElementById('contactForm').style.display !== 'none') {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
}

/**
 * Load faculty data from backend API
 * Uses fetch() to send GET request to /api/faculty
 */
/**
 * Load faculty data from backend API
 * Uses fetch() to send GET request to /api/faculty
 */
function loadFacultyFromAPI() {
    const facultyGrid = document.getElementById('facultyGrid');
    const hodContainer = document.getElementById('hodContainer');

    // Only run on faculty page
    if (!facultyGrid || !hodContainer) return;

    console.log('📡 Loading faculty from API...');
    showLoader();

    fetch(`${API_BASE_URL}/api/faculty`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.success && data.data.length > 0) {
                console.log('✅ Loaded', data.count, 'faculty members from database');

                // Clear initial markers
                facultyGrid.innerHTML = '';
                // Only clear HOD if we have HOD data in response
                const hasHod = data.data.some(member => member.is_hod);
                if (hasHod) {
                    hodContainer.innerHTML = '';
                }

                let facultyHtml = '';
                let hodHtml = '';

                data.data.forEach(function (member) {
                    const avatarEmoji = member.is_hod ? '👨‍🎓' : (member.name.toLowerCase().includes('ms.') || member.name.toLowerCase().includes('dr. priya') ? '👩‍🏫' : '👨‍🏫');

                    if (member.is_hod) {
                        hodHtml += `
                            <div class="faculty-card featured">
                                <div class="faculty-avatar">
                                    <div class="avatar-placeholder">${avatarEmoji}</div>
                                </div>
                                <div class="faculty-info">
                                    <h3>${member.name}</h3>
                                    <span class="faculty-designation">${member.designation}</span>
                                    <span class="faculty-subject">${member.subject}</span>
                                    <p class="faculty-bio">${member.bio || ''}</p>
                                    <div class="faculty-contact">
                                        <span>📧 ${member.email || ''}</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        facultyHtml += `
                            <div class="faculty-card">
                                <div class="faculty-avatar">
                                    <div class="avatar-placeholder">${avatarEmoji}</div>
                                </div>
                                <div class="faculty-info">
                                    <h3>${member.name}</h3>
                                    <span class="faculty-designation">${member.designation}</span>
                                    <span class="faculty-subject">${member.subject}</span>
                                    <p class="faculty-bio">${member.bio || ''}</p>
                                </div>
                            </div>
                        `;
                    }
                });

                // Update DOM
                hodContainer.innerHTML = hodHtml || '<p class="text-center">Department leadership information coming soon.</p>';
                facultyGrid.innerHTML = facultyHtml || '<p class="text-center">Faculty details coming soon.</p>';

                // Re-initialize scroll animations for new elements
                initScrollAnimations();

                console.log('✅ Faculty UI updated with', data.count, 'members');
            }
        })
        .catch(function (error) {
            console.log('⚠️ Could not load faculty from API');
            console.log('Error:', error);
            facultyGrid.innerHTML = '<p class="text-center">Error loading faculty data. Please try again later.</p>';
        })
        .finally(function () {
            hideLoader();
        });
}

/**
 * Fetch all contact messages (for admin use)
 */
function getContactMessages() {
    showLoader();
    fetch(`${API_BASE_URL}/api/contact`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.success) {
                console.log('📧 Contact Messages:', data.data);
                return data.data;
            }
        })
        .catch(function (error) {
            console.log('Error fetching messages:', error);
        })
        .finally(() => hideLoader());
}

// =====================================================
// Kinetic Dots Loader Management
// =====================================================

/**
 * Initialize and inject the loader overlay into the DOM
 */
function initLoader() {
    if (document.getElementById('loaderOverlay')) return;

    const loaderHtml = `
        <div id="loaderOverlay" class="loader-overlay">
            <div class="loader-container">
                <div class="loader-dots-flex">
                    <div class="dot-wrapper"><div class="bouncing-dot"><div class="dot-inner"></div></div><div class="floor-ripple"></div><div class="reflective-shadow"></div></div>
                    <div class="dot-wrapper"><div class="bouncing-dot"><div class="dot-inner"></div></div><div class="floor-ripple"></div><div class="reflective-shadow"></div></div>
                    <div class="dot-wrapper"><div class="bouncing-dot"><div class="dot-inner"></div></div><div class="floor-ripple"></div><div class="reflective-shadow"></div></div>
                    <div class="dot-wrapper"><div class="bouncing-dot"><div class="dot-inner"></div></div><div class="floor-ripple"></div><div class="reflective-shadow"></div></div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loaderHtml);
}

/**
 * Show the loader overlay
 */
function showLoader() {
    const loader = document.getElementById('loaderOverlay');
    if (loader) loader.classList.add('active');
}

/**
 * Hide the loader overlay
 */
function hideLoader() {
    const loader = document.getElementById('loaderOverlay');
    if (loader) loader.classList.remove('active');
}

// Load faculty when on faculty page
document.addEventListener('DOMContentLoaded', function () {
    loadFacultyFromAPI();
});

// =====================================================
// Console welcome message
// =====================================================
console.log('%c🤖 AI & DS Department Website', 'font-size: 20px; font-weight: bold; color: #6366f1;');
console.log('%cBuilt with HTML, CSS, JavaScript & Flask Backend', 'font-size: 12px; color: #64748b;');
console.log('%c📡 Backend API: ' + API_BASE_URL, 'font-size: 12px; color: #10b981;');


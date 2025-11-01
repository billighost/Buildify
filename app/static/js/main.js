// Main JavaScript for animations and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });
    loadNotificationDropdown();
        
    // Refresh notifications every 30 seconds if user is authenticated
    if (document.getElementById('notificationDropdown')) {
        setInterval(loadNotificationDropdown, 30000);
    }

    // Loading screen
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('fade-out');
            setTimeout(() => {
                loadingScreen.remove();
            }, 500);
        }, 2000);
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.custom-navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // // Custom cursor
    // if (window.innerWidth > 768) {
    //     const cursorDot = document.createElement('div');
    //     const cursorOutline = document.createElement('div');
    //     cursorDot.classList.add('cursor-dot');
    //     cursorOutline.classList.add('cursor-outline');
    //     document.body.appendChild(cursorDot);
    //     document.body.appendChild(cursorOutline);

    //     document.addEventListener('mousemove', (e) => {
    //         cursorDot.style.left = e.clientX + 'px';
    //         cursorDot.style.top = e.clientY + 'px';
            
    //         cursorOutline.style.left = e.clientX + 'px';
    //         cursorOutline.style.top = e.clientY + 'px';
    //     });

    //     document.addEventListener('mousedown', () => {
    //         cursorDot.style.transform = 'scale(0.5)';
    //         cursorOutline.style.transform = 'scale(1.2)';
    //     });

    //     document.addEventListener('mouseup', () => {
    //         cursorDot.style.transform = 'scale(1)';
    //         cursorOutline.style.transform = 'scale(1)';
    //     });

    //     // Hover effects
    //     const hoverElements = document.querySelectorAll('button, a, .card, .feature-card');
    //     hoverElements.forEach(el => {
    //         el.addEventListener('mouseenter', () => {
    //             cursorDot.style.transform = 'scale(1.5)';
    //             cursorOutline.style.transform = 'scale(1.5)';
    //         });
    //         el.addEventListener('mouseleave', () => {
    //             cursorDot.style.transform = 'scale(1)';
    //             cursorOutline.style.transform = 'scale(1)';
    //         });
    //     });
    // }

    // Counter animation for stats
    const animateCounters = () => {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.ceil(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            };

            updateCounter();
        });
    };

    // Intersection Observer for counters
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        });

        observer.observe(statsSection);
    }

    // Parallax effect
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.getAttribute('data-speed') || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });

    // Theme toggle (if needed later)
    const themeToggle = document.createElement('button');
        themeToggle.innerHTML = '<i class="bi bi-moon"></i>';
        themeToggle.className = 'btn btn-sm btn-outline-secondary theme-toggle';
        themeToggle.style.position = 'fixed';
        themeToggle.style.bottom = '20px';
        themeToggle.style.right = '20px';
        themeToggle.style.zIndex = '1000';
        
        themeToggle.addEventListener('click', () => {
            document.documentElement.setAttribute('data-bs-theme', 
                document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
            );
            themeToggle.innerHTML = document.documentElement.getAttribute('data-bs-theme') === 'dark' 
                ? '<i class="bi bi-sun"></i>' 
                : '<i class="bi bi-moon"></i>';
        });


        document.body.appendChild(themeToggle);
        
    });
    // Add to the dashboard scripts
    function compareProjects() {
        const selectedProjects = Array.from(document.querySelectorAll('.project-checkbox:checked')).map(cb => cb.value);
        
        if (selectedProjects.length < 2) {
            showNotification('Please select at least 2 projects to compare', 'warning');
            return;
        }
        
        // Store selected projects in sessionStorage for the comparison page
        sessionStorage.setItem('compareProjects', JSON.stringify(selectedProjects));
        window.location.href = "{{ url_for('projects.projects_comparison') }}";
    }

    // Notification functions
    function loadNotificationDropdown() {
        if (document.getElementById('notification-list')) {
            fetch('/api/notifications?limit=5&unread_only=false')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const notificationList = document.getElementById('notification-list');
                        if (data.notifications.length === 0) {
                            notificationList.innerHTML = `
                                <div class="text-center p-3 text-muted">
                                    <i class="bi bi-bell-slash d-block mb-2"></i>
                                    No notifications
                                </div>
                            `;
                        } else {
                            notificationList.innerHTML = data.notifications.map(notification => `
                                <a class="dropdown-item notification-dropdown-item ${notification.is_read ? '' : 'fw-bold'}" 
                                href="${notification.action_url || '#'}" 
                                onclick="markNotificationRead(${notification.id})">
                                    <div class="d-flex w-100 justify-content-between">
                                        <h6 class="mb-1">${notification.title}</h6>
                                        <small>${notification.time_ago}</small>
                                    </div>
                                    <p class="mb-1 small">${notification.message}</p>
                                </a>
                            `).join('');
                        }
                        
                        // Update notification badge
                        updateNotificationBadge(data.unread_count);
                    }
                })
                .catch(error => {
                    console.error('Error loading notifications:', error);
                });
        }
    }

    function updateNotificationBadge(count) {
        const badge = document.querySelector('#notificationDropdown .badge');
        const bellIcon = document.querySelector('#notificationDropdown i.bi-bell');
        
        if (count > 0) {
            if (badge) {
                badge.textContent = count;
            } else if (bellIcon) {
                const newBadge = document.createElement('span');
                newBadge.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger';
                newBadge.textContent = count;
                newBadge.innerHTML += '<span class="visually-hidden">unread notifications</span>';
                bellIcon.parentNode.appendChild(newBadge);
            }
        } else if (badge) {
            badge.remove();
        }
    }
    // Mark notification as read
    function markNotificationRead(notificationId) {
        fetch(`/api/notifications/${notificationId}/read`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload notifications
                loadNotifications();
                // Update the notification item in the list
                const item = document.querySelector(`.notification-item[data-notification-id="${notificationId}"]`);
                if (item) {
                    item.classList.remove('bg-light', 'fw-bold');
                    const badge = item.querySelector('.badge');
                    if (badge) badge.remove();
                }
            }
        });
    }

    // Mark all notifications as read
    function markAllNotificationsRead() {
        fetch('/api/notifications/read-all', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadNotifications();
                // Update all notification items
                document.querySelectorAll('.notification-item').forEach(item => {
                    item.classList.remove('bg-light', 'fw-bold');
                    const badge = item.querySelector('.badge');
                    if (badge) badge.remove();
                });
                showToast('All notifications marked as read', 'success');
            }
        });
    }

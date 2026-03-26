/* ============================================================
   TravelUp Frontend – script.js
   API base URL: change this if your backend runs elsewhere
   ============================================================ */
const API = 'http://127.0.0.1:8000';

/* ── State ── */
let state = {
    token: localStorage.getItem('tu_token') || null,
    user: JSON.parse(localStorage.getItem('tu_user') || 'null'),
    isAdmin: false,
    destinations: [],          // cached for filtering
    roles: [],                 // cached admin roles list
};

/* ============================================================
   BOOTSTRAP
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
    /* Auth forms */
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);

    /* Main forms */
    document.getElementById('booking-form').addEventListener('submit', handleBooking);
    document.getElementById('review-form').addEventListener('submit', handleReview);
    document.getElementById('profile-form').addEventListener('submit', handleProfileUpdate);
    document.getElementById('pay-form').addEventListener('submit', handlePayment);

    /* Admin forms */
    document.getElementById('add-dest-form').addEventListener('submit', handleAddDestination);
    document.getElementById('edit-dest-form').addEventListener('submit', handleEditDestination);

    /* Star picker */
    document.querySelectorAll('.star').forEach(s =>
        s.addEventListener('click', () => setStarRating(+s.dataset.value))
    );

    /* Booking date validation */
    document.getElementById('book-start').addEventListener('change', () => {
        document.getElementById('book-end').min = document.getElementById('book-start').value;
    });

    /* Boot */
    if (state.token) {
        bootApp();
    } else {
        showAuth();
    }
});

/* ============================================================
   AUTH
   ============================================================ */
async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('login-btn');
    setLoading(btn, true);

    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;

    try {
        const data = await api('POST', '/auth/login', { username, password }, false);
        state.token = data.access_token;
        localStorage.setItem('tu_token', state.token);
        toast('Welcome back!', 'success');
        document.getElementById('login-form').reset();
        await bootApp();
    } catch (err) {
        toast(err.message || 'Login failed', 'error');
    } finally {
        setLoading(btn, false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('register-btn');
    setLoading(btn, true);

    const username = document.getElementById('register-username').value.trim();
    const password = document.getElementById('register-password').value;

    try {
        await api('POST', '/auth/register', { username, password }, false);
        toast('Account created! Please log in.', 'success');
        document.getElementById('register-form').reset();
        switchTab('login');
    } catch (err) {
        toast(err.message || 'Registration failed', 'error');
    } finally {
        setLoading(btn, false);
    }
}

function logout() {
    state.token = null;
    state.user = null;
    state.isAdmin = false;
    localStorage.removeItem('tu_token');
    localStorage.removeItem('tu_user');
    showAuth();
    document.getElementById('navbar').classList.add('hidden');
    toast('Logged out');
}

/* Switching login/register tabs */
function switchTab(tab) {
    document.getElementById('form-login').classList.toggle('hidden', tab !== 'login');
    document.getElementById('form-register').classList.toggle('hidden', tab !== 'register');
    document.getElementById('tab-login').classList.toggle('active', tab === 'login');
    document.getElementById('tab-register').classList.toggle('active', tab === 'register');
}

/* ============================================================
   BOOT – fetch profile, set isAdmin, show app
   ============================================================ */
async function bootApp() {
    showLoader(true);
    try {
        const profile = await api('GET', '/profile');
        /* Profile returns UserProfile which joins Username via user_id.
           We also need username – fetch from admin/users if admin, else derive. */
        state.user = profile;
        localStorage.setItem('tu_user', JSON.stringify(profile));

        /* Try admin route to detect admin status */
        try {
            await api('GET', '/admin/users');
            state.isAdmin = true;
        } catch { state.isAdmin = false; }

        applyUserUI();
        showApp();
        navigate('destinations');
    } catch (err) {
        /* Token might be expired */
        toast('Session expired – please login again', 'warn');
        logout();
    } finally {
        showLoader(false);
    }
}

function applyUserUI() {
    const navbar = document.getElementById('navbar');
    navbar.classList.remove('hidden');

    const username = state.user?.username || state.user?.first_name || 'User';
    document.getElementById('nav-username-label').textContent = username;
    document.getElementById('nav-avatar').textContent = username[0].toUpperCase();
    document.getElementById('profile-big-avatar').textContent = username[0].toUpperCase();
    document.getElementById('profile-username-display').textContent = username;

    const adminNavLink = document.getElementById('nav-admin');
    if (state.isAdmin) {
        adminNavLink.classList.remove('hidden');
        document.getElementById('profile-role-badge').textContent = '⚙ Admin';
        document.getElementById('profile-role-badge').className = 'badge badge-admin';
    } else {
        adminNavLink.classList.add('hidden');
        document.getElementById('profile-role-badge').textContent = 'Member';
        document.getElementById('profile-role-badge').className = 'badge badge-blue';
    }
}

/* ============================================================
   NAVIGATION
   ============================================================ */
function navigate(view) {
    /* Hide all app views */
    document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));

    /* Update nav active state */
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    const navEl = document.getElementById(`nav-${view}`);
    if (navEl) navEl.classList.add('active');

    /* Show the target view */
    const el = document.getElementById(`view-${view}`);
    if (el) { el.classList.remove('hidden'); }

    /* Load data */
    if (view === 'destinations')  loadDestinations();
    if (view === 'bookings')      loadBookings();
    if (view === 'payments')      loadPayments();
    if (view === 'profile')       loadProfile();
    if (view === 'admin')         loadAdmin();

    /* Close mobile nav */
    document.getElementById('nav-links').classList.remove('open');
}

function toggleNav() {
    document.getElementById('nav-links').classList.toggle('open');
}

/* ============================================================
   DESTINATIONS
   ============================================================ */
async function loadDestinations() {
    const grid = document.getElementById('destinations-grid');
    const loader = document.getElementById('dest-loader');
    grid.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const dests = await api('GET', '/destinations');
        state.destinations = dests;
        renderDestinations(dests);
    } catch (err) {
        grid.innerHTML = `<p class="empty-state">${err.message}</p>`;
    } finally {
        loader.classList.add('hidden');
    }
}

function renderDestinations(dests) {
    const grid = document.getElementById('destinations-grid');
    grid.innerHTML = '';

    if (!dests.length) {
        grid.innerHTML = '<p class="empty-state" style="grid-column:1/-1">No destinations found.</p>';
        return;
    }

    dests.forEach(d => {
        const card = document.createElement('div');
        card.className = 'dest-card';
        const imgSrc = d.cover_image || '';
        card.innerHTML = `
            <div class="dest-thumb">
                ${imgSrc
                    ? `<img src="${esc(imgSrc)}" alt="${esc(d.title || d.city)}" onerror="this.parentElement.innerHTML='🌍'">`
                    : '🌍'}
            </div>
            <div class="dest-body">
                <h3>${esc(d.title || d.city)}</h3>
                <div class="dest-country">📍 ${esc(d.city)}, ${esc(d.country)}</div>
                ${d.description ? `<div class="dest-desc">${esc(d.description)}</div>` : ''}
                <span class="badge rating-badge">⭐ ${d.rating ?? '—'}</span>
            </div>
            <div class="dest-footer">
                <button class="btn btn-ghost btn-sm" onclick="openReviewsModal(${d.id}, '${esc(d.title || d.city)}')">Reviews</button>
                <button class="btn btn-primary btn-sm" onclick="openBookModal(${d.id}, '${esc(d.title || d.city)}')">Book Now</button>
            </div>`;
        grid.appendChild(card);
    });
}

function filterDestinations() {
    const city    = document.getElementById('filter-city').value.toLowerCase();
    const country = document.getElementById('filter-country').value.toLowerCase();
    const rating  = parseFloat(document.getElementById('filter-rating').value) || 0;

    const filtered = state.destinations.filter(d =>
        (!city    || d.city.toLowerCase().includes(city)) &&
        (!country || d.country.toLowerCase().includes(country)) &&
        (!rating  || (d.rating ?? 0) >= rating)
    );
    renderDestinations(filtered);
}

function clearFilters() {
    ['filter-city','filter-country','filter-rating'].forEach(id =>
        document.getElementById(id).value = '');
    renderDestinations(state.destinations);
}

/* ============================================================
   BOOK MODAL
   ============================================================ */
function openBookModal(destId, city) {
    document.getElementById('book-dest-id').value = destId;
    document.getElementById('modal-book-title').textContent = `Book Destination – ${city}`;
    /* Set minimum start date to today */
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('book-start').min = today;
    openModal('modal-book');
}

async function handleBooking(e) {
    e.preventDefault();
    const btn = e.submitter || e.target.querySelector('button[type=submit]');
    setLoading(btn, true);

    const body = {
        destination_id:  +document.getElementById('book-dest-id').value,
        start_date:       document.getElementById('book-start').value,
        end_date:         document.getElementById('book-end').value,
        travelers_count:  +document.getElementById('book-travelers').value,
        total_price:      +document.getElementById('book-price').value,
    };

    try {
        await api('POST', '/bookings', body);
        toast('Booking confirmed! 🎉', 'success');
        closeModal('modal-book');
        document.getElementById('booking-form').reset();
    } catch (err) {
        toast(err.message, 'error');
    } finally {
        setLoading(btn, false);
    }
}

/* ============================================================
   BOOKINGS
   ============================================================ */
async function loadBookings() {
    const tbody  = document.getElementById('bookings-tbody');
    const loader = document.getElementById('bookings-loader');
    const empty  = document.getElementById('bookings-empty');
    tbody.innerHTML = '';
    empty.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const bookings = await api('GET', '/bookings/my');
        loader.classList.add('hidden');

        if (!bookings.length) { empty.classList.remove('hidden'); return; }

        bookings.forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${b.id}</td>
                <td>${b.destination_id}</td>
                <td>${b.start_date}</td>
                <td>${b.end_date}</td>
                <td>${b.travelers_count}</td>
                <td>$${(+b.total_price).toFixed(2)}</td>
                <td>${statusBadge(b.status)}</td>
                <td>
                    <div class="action-btns">
                        ${b.status !== 'cancelled'
                            ? `<button class="btn btn-danger btn-sm" onclick="cancelBooking(${b.id})">Cancel</button>
                               <button class="btn btn-ghost btn-sm" onclick="openPayModal(${b.id}, ${b.total_price})">Pay</button>`
                            : '<span class="text-muted">—</span>'}
                    </div>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

async function cancelBooking(id) {
    if (!confirm('Cancel this booking?')) return;
    try {
        await api('PATCH', `/bookings/${id}/cancel`);
        toast('Booking cancelled', 'warn');
        loadBookings();
    } catch (err) { toast(err.message, 'error'); }
}

/* ============================================================
   PAYMENTS
   ============================================================ */
function openPayModal(bookingId, amount) {
    document.getElementById('pay-booking-id').value = bookingId;
    document.getElementById('pay-amount').value = amount || '';
    openModal('modal-pay');
}

async function handlePayment(e) {
    e.preventDefault();
    const btn = e.submitter;
    setLoading(btn, true);

    try {
        await api('POST', '/payments', {
            booking_id: +document.getElementById('pay-booking-id').value,
            amount:      +document.getElementById('pay-amount').value,
            currency:     document.getElementById('pay-currency').value,
            provider:     document.getElementById('pay-provider').value,
        });
        toast('Payment recorded! ✅', 'success');
        closeModal('modal-pay');
        document.getElementById('pay-form').reset();
    } catch (err) {
        toast(err.message, 'error');
    } finally {
        setLoading(btn, false);
    }
}

async function loadPayments() {
    const tbody  = document.getElementById('payments-tbody');
    const loader = document.getElementById('payments-loader');
    const empty  = document.getElementById('payments-empty');
    tbody.innerHTML = '';
    empty.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const payments = await api('GET', '/payments/my');
        loader.classList.add('hidden');

        if (!payments.length) { empty.classList.remove('hidden'); return; }

        payments.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${p.id}</td>
                <td>#${p.booking_id}</td>
                <td>$${(+p.amount).toFixed(2)}</td>
                <td>${esc(p.currency)}</td>
                <td>${esc(p.provider)}</td>
                <td>${statusBadge(p.status)}</td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

/* ============================================================
   REVIEWS
   ============================================================ */
async function openReviewsModal(destId, city) {
    document.getElementById('modal-reviews-title').textContent = `Reviews – ${city}`;
    document.getElementById('review-dest-id').value = destId;
    setStarRating(0);
    document.getElementById('review-comment').value = '';
    openModal('modal-reviews');
    await loadReviews(destId);
}

async function loadReviews(destId) {
    const list = document.getElementById('reviews-list');
    list.innerHTML = '<p class="text-muted">Loading…</p>';

    try {
        const reviews = await api('GET', `/destinations/${destId}/reviews`, null, false);
        if (!reviews.length) {
            list.innerHTML = '<p class="text-muted">No reviews yet. Be the first!</p>';
            return;
        }
        list.innerHTML = '';
        reviews.forEach(r => {
            const el = document.createElement('div');
            el.className = 'review-item';
            el.innerHTML = `
                <div class="avatar">${(r.username || 'U')[0].toUpperCase()}</div>
                <div class="review-item-body">
                    <div class="username">${esc(r.username || 'User')}</div>
                    <div class="stars">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</div>
                    <div class="comment">${esc(r.comment || '')}</div>
                </div>
                ${state.isAdmin ? `<button class="btn btn-danger btn-sm review-delete" onclick="deleteReview(${r.id}, ${destId})">✕</button>` : ''}`;
            list.appendChild(el);
        });
    } catch (err) {
        list.innerHTML = `<p class="text-muted">${err.message}</p>`;
    }
}

async function handleReview(e) {
    e.preventDefault();
    const rating  = +document.getElementById('review-rating').value;
    const comment = document.getElementById('review-comment').value.trim();
    const destId  = +document.getElementById('review-dest-id').value;

    if (!rating) { toast('Please select a star rating', 'warn'); return; }

    try {
        await api('POST', '/reviews', { destination_id: destId, rating, comment });
        toast('Review submitted!', 'success');
        setStarRating(0);
        document.getElementById('review-comment').value = '';
        await loadReviews(destId);
    } catch (err) { toast(err.message, 'error'); }
}

async function deleteReview(id, destId) {
    if (!confirm('Delete this review?')) return;
    try {
        await api('DELETE', `/reviews/${id}`);
        toast('Review deleted', 'warn');
        await loadReviews(destId);
    } catch (err) { toast(err.message, 'error'); }
}

function setStarRating(val) {
    document.getElementById('review-rating').value = val;
    document.querySelectorAll('.star').forEach(s => {
        s.classList.toggle('active', +s.dataset.value <= val);
    });
}

/* ============================================================
   PROFILE
   ============================================================ */
async function loadProfile() {
    try {
        const profile = await api('GET', '/profile');
        document.getElementById('profile-first-name').value = profile.first_name || '';
        document.getElementById('profile-last-name').value  = profile.last_name  || '';
        document.getElementById('profile-bio').value        = profile.bio         || '';
        document.getElementById('profile-phone').value      = profile.phone       || '';
    } catch (err) { toast(err.message, 'error'); }
}

async function handleProfileUpdate(e) {
    e.preventDefault();
    const btn = e.submitter;
    setLoading(btn, true);

    const body = {
        first_name: document.getElementById('profile-first-name').value || null,
        last_name:  document.getElementById('profile-last-name').value  || null,
        bio:        document.getElementById('profile-bio').value         || null,
        phone:      document.getElementById('profile-phone').value       || null,
    };

    try {
        await api('PATCH', '/profile/update', body);
        toast('Profile updated!', 'success');
    } catch (err) { toast(err.message, 'error'); }
    finally { setLoading(btn, false); }
}

/* ============================================================
   ADMIN PANEL
   ============================================================ */
let currentAdminTab = 'users';

async function loadAdmin() {
    /* Load roles for assignment dropdowns */
    try {
        state.roles = await api('GET', '/admin/roles');
    } catch {}
    switchAdminTab('users');
}

function switchAdminTab(tab) {
    currentAdminTab = tab;
    document.querySelectorAll('.admin-panel-content').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.admin-tab').forEach(el => el.classList.remove('active'));

    document.getElementById(`admin-tab-${tab}`).classList.remove('hidden');

    /* Activate corresponding button */
    document.querySelectorAll('.admin-tab').forEach(btn => {
        if (btn.textContent.toLowerCase().replace(/\s+/g, '-') === tab ||
            btn.getAttribute('onclick')?.includes(`'${tab}'`)) {
            btn.classList.add('active');
        }
    });

    if (tab === 'users')        loadAdminUsers();
    if (tab === 'destinations') loadAdminDestinations();
    if (tab === 'all-bookings') loadAdminBookings();
    if (tab === 'all-payments') loadAdminPayments();
}

/* ─── Admin: Users ─── */
async function loadAdminUsers() {
    const tbody  = document.getElementById('admin-users-tbody');
    const loader = document.getElementById('admin-users-loader');
    tbody.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const users = await api('GET', '/admin/users');
        loader.classList.add('hidden');

        users.forEach(u => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${u.id}</td>
                <td><strong>${esc(u.username)}</strong></td>
                <td>${u.roles.map(r => `<span class="badge badge-blue">${esc(r)}</span>`).join(' ') || '—'}</td>
                <td>${u.permissions.map(p => `<span class="badge badge-gray">${esc(p)}</span>`).join(' ') || '—'}</td>
                <td>${u.is_admin ? '<span class="badge badge-admin">Admin</span>' : '—'}</td>
                <td>
                    <div class="action-btns">
                        <button class="btn btn-ghost btn-sm" onclick="openAssignRole(${u.id}, '${esc(u.username)}')">Assign Role</button>
                        ${!u.is_admin ? `<button class="btn btn-ghost btn-sm" onclick="makeAdmin(${u.id})">Make Admin</button>` : ''}
                        <button class="btn btn-danger btn-sm" onclick="deleteUser(${u.id})">Delete</button>
                    </div>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

async function makeAdmin(userId) {
    if (!confirm('Promote this user to admin?')) return;
    try {
        await api('POST', `/admin/make-admin?user_id=${userId}`);
        toast('User is now admin!', 'success');
        loadAdminUsers();
    } catch (err) { toast(err.message, 'error'); }
}

async function deleteUser(userId) {
    if (!confirm('Permanently delete this user?')) return;
    try {
        await api('DELETE', `/admin/users/${userId}`);
        toast('User deleted', 'warn');
        loadAdminUsers();
    } catch (err) { toast(err.message, 'error'); }
}

function openAssignRole(userId, username) {
    document.getElementById('assign-role-user-id').value = userId;
    document.getElementById('modal-assign-role-title').textContent = `Assign Role – ${username}`;
    const sel = document.getElementById('assign-role-select');
    sel.innerHTML = state.roles.map(r =>
        `<option value="${r.id}">${esc(r.name)}</option>`).join('');
    openModal('modal-assign-role');
}

async function submitAssignRole() {
    const userId = +document.getElementById('assign-role-user-id').value;
    const roleId = +document.getElementById('assign-role-select').value;

    try {
        await api('POST', '/admin/set-role', { user_id: userId, role_id: roleId });
        toast('Role assigned!', 'success');
        closeModal('modal-assign-role');
        loadAdminUsers();
    } catch (err) { toast(err.message, 'error'); }
}

/* ─── Admin: Destinations ─── */
async function loadAdminDestinations() {
    const tbody  = document.getElementById('admin-dest-tbody');
    const loader = document.getElementById('admin-dest-loader');
    tbody.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const dests = await api('GET', '/destinations');
        loader.classList.add('hidden');

        dests.forEach(d => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${d.id}</td>
                <td>${esc(d.title || '—')}</td>
                <td>${esc(d.city)}</td>
                <td>${esc(d.country)}</td>
                <td><span class="badge rating-badge">⭐ ${d.rating ?? '—'}</span></td>
                <td>
                    <div class="action-btns">
                        <button class="btn btn-ghost btn-sm" onclick="openEditDest(${d.id},'${esc(d.title||'')}','${esc(d.city)}','${esc(d.country)}',${d.rating??0},'${esc(d.description||'')}','${esc(d.cover_image||'')}')">Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteDestination(${d.id})">Delete</button>
                    </div>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

async function handleAddDestination(e) {
    e.preventDefault();
    const btn = e.submitter;
    setLoading(btn, true);

    try {
        await api('POST', '/destinations', {
            title:       document.getElementById('dest-title').value,
            city:        document.getElementById('dest-city').value,
            country:     document.getElementById('dest-country').value,
            cover_image: document.getElementById('dest-cover-image').value,
            rating:      +document.getElementById('dest-rating').value,
            description: document.getElementById('dest-description').value,
        });
        toast('Destination added!', 'success');
        document.getElementById('add-dest-form').reset();
        loadAdminDestinations();
    } catch (err) { toast(err.message, 'error'); }
    finally { setLoading(btn, false); }
}

function openEditDest(id, title, city, country, rating, description, cover_image) {
    document.getElementById('edit-dest-id').value          = id;
    document.getElementById('edit-dest-title').value       = title;
    document.getElementById('edit-dest-city').value        = city;
    document.getElementById('edit-dest-country').value     = country;
    document.getElementById('edit-dest-rating').value      = rating;
    document.getElementById('edit-dest-description').value = description;
    document.getElementById('edit-dest-cover-image').value = cover_image || '';
    openModal('modal-edit-dest');
}

async function handleEditDestination(e) {
    e.preventDefault();
    const id  = document.getElementById('edit-dest-id').value;
    const btn = e.submitter;
    setLoading(btn, true);

    try {
        await api('PUT', `/destinations/${id}`, {
            title:       document.getElementById('edit-dest-title').value,
            city:        document.getElementById('edit-dest-city').value,
            country:     document.getElementById('edit-dest-country').value,
            cover_image: document.getElementById('edit-dest-cover-image').value,
            rating:      +document.getElementById('edit-dest-rating').value,
            description: document.getElementById('edit-dest-description').value,
        });
        toast('Destination updated!', 'success');
        closeModal('modal-edit-dest');
        loadAdminDestinations();
    } catch (err) { toast(err.message, 'error'); }
    finally { setLoading(btn, false); }
}

async function deleteDestination(id) {
    if (!confirm('Delete this destination? This cannot be undone.')) return;
    try {
        await api('DELETE', `/destinations/${id}`);
        toast('Destination deleted', 'warn');
        loadAdminDestinations();
    } catch (err) { toast(err.message, 'error'); }
}

/* ─── Admin: All Bookings ─── */
async function loadAdminBookings() {
    const tbody  = document.getElementById('admin-bookings-tbody');
    const loader = document.getElementById('admin-bookings-loader');
    tbody.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const bookings = await api('GET', '/bookings');
        loader.classList.add('hidden');

        bookings.forEach(b => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${b.id}</td>
                <td>#${b.user_id}</td>
                <td>#${b.destination_id}</td>
                <td>${b.start_date}</td>
                <td>${b.end_date}</td>
                <td>${b.travelers_count}</td>
                <td>$${(+b.total_price).toFixed(2)}</td>
                <td>${statusBadge(b.status)}</td>
                <td>
                    <select class="status-select" onchange="updateBookingStatus(${b.id}, this.value)">
                        <option value="pending"   ${b.status==='pending'   ? 'selected':''}>Pending</option>
                        <option value="confirmed" ${b.status==='confirmed' ? 'selected':''}>Confirmed</option>
                        <option value="cancelled" ${b.status==='cancelled' ? 'selected':''}>Cancelled</option>
                        <option value="completed" ${b.status==='completed' ? 'selected':''}>Completed</option>
                    </select>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

async function updateBookingStatus(id, status) {
    try {
        await api('PATCH', `/bookings/${id}/status`, { status });
        toast(`Status updated to "${status}"`, 'success');
    } catch (err) { toast(err.message, 'error'); }
}

/* ─── Admin: All Payments ─── */
async function loadAdminPayments() {
    const tbody  = document.getElementById('admin-payments-tbody');
    const loader = document.getElementById('admin-payments-loader');
    tbody.innerHTML = '';
    loader.classList.remove('hidden');

    try {
        const payments = await api('GET', '/payments');
        loader.classList.add('hidden');

        if (!payments.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="empty-state">No payments yet.</td></tr>';
            return;
        }

        payments.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${p.id}</td>
                <td>#${p.user_id}</td>
                <td>#${p.booking_id}</td>
                <td>$${(+p.amount).toFixed(2)}</td>
                <td>${esc(p.currency)}</td>
                <td>${esc(p.provider)}</td>
                <td>${statusBadge(p.status)}</td>`;
            tbody.appendChild(tr);
        });
    } catch (err) {
        loader.classList.add('hidden');
        toast(err.message, 'error');
    }
}

/* ============================================================
   MODALS
   ============================================================ */
function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
}

function closeModal(id, event) {
    /* If called from overlay click, only close if click is on overlay itself */
    if (event && event.target !== event.currentTarget) return;
    document.getElementById(id).classList.add('hidden');
}

/* Close modals with Escape key */
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay:not(.hidden)')
            .forEach(m => m.classList.add('hidden'));
    }
});

/* ============================================================
   API HELPER
   ============================================================ */
async function api(method, path, body = null, auth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth && state.token) headers['Authorization'] = `Bearer ${state.token}`;

    const opts = { method, headers };
    if (body !== null && method !== 'GET') opts.body = JSON.stringify(body);

    const res = await fetch(`${API}${path}`, opts);

    if (res.status === 401) {
        logout();
        throw new Error('Session expired');
    }

    if (!res.ok) {
        let message = `Request failed (${res.status})`;
        try {
            const json = await res.json();
            message = json.detail || JSON.stringify(json);
        } catch {}
        throw new Error(message);
    }

    /* 204 or empty body */
    const text = await res.text();
    return text ? JSON.parse(text) : null;
}

/* ============================================================
   UI HELPERS
   ============================================================ */
function showAuth() {
    document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
    document.getElementById('view-auth').classList.remove('hidden');
    document.getElementById('navbar').classList.add('hidden');
}

function showApp() {
    document.getElementById('view-auth').classList.add('hidden');
}

function showLoader(show) {
    document.getElementById('page-loader').classList.toggle('hidden', !show);
}

let toastTimer;
function toast(msg, type = '') {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.className = `toast ${type} show`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        el.classList.remove('show');
    }, 3500);
}

function setLoading(btn, loading) {
    if (!btn) return;
    btn.disabled = loading;
    if (loading) {
        btn._original = btn.textContent;
        btn.textContent = 'Loading…';
    } else {
        btn.textContent = btn._original || btn.textContent;
    }
}

function statusBadge(status) {
    const map = {
        active:    'badge-green',
        confirmed: 'badge-green',
        completed: 'badge-blue',
        pending:   'badge-yellow',
        cancelled: 'badge-red',
        paid:      'badge-green',
        failed:    'badge-red',
    };
    const cls = map[(status || '').toLowerCase()] || 'badge-gray';
    return `<span class="badge ${cls}">${status || '—'}</span>`;
}

function esc(str) {
    return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

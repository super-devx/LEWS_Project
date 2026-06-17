file_path = r'C:\Users\DELL\OneDrive\Desktop\LEWS_projectt\LEWS_Project\01022021_website\user_entry\static\css\landing-style.css'

css_content = '''
/* ===== FUNDING ORGANIZATIONS SECTION ===== */
.funding-section {
    position: relative;
    z-index: 10;
    width: 100%;
}

.funding-banner-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-4);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease-out;
}

.funding-banner-wrapper.animate-fade-in-up {
    opacity: 1;
    transform: translateY(0);
}

.funding-line-left,
.funding-line-right {
    height: 2px;
    width: 80px;
    background: var(--color-accent-500);
    position: relative;
}

.funding-line-left::after,
.funding-line-right::before {
    content: '';
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 8px;
    height: 8px;
    background: var(--color-accent-500);
    border-radius: 50%;
}

.funding-line-left::after {
    right: 0;
}

.funding-line-right::before {
    left: 0;
}

.funding-banner {
    background: linear-gradient(135deg, var(--color-primary-900), var(--color-primary-800));
    color: var(--color-accent-400);
    font-family: var(--font-primary);
    font-weight: 700;
    font-size: 1.25rem;
    padding: var(--space-3) var(--space-8);
    border-radius: 50px;
    border: 1px solid rgba(255, 122, 47, 0.3);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 0 0 10px rgba(255, 122, 47, 0.1);
}

.funding-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: var(--space-4);
    margin-top: var(--space-6);
}

@media (max-width: 1200px) {
    .funding-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .funding-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 576px) {
    .funding-grid {
        grid-template-columns: 1fr;
    }
}

.funding-card {
    background: var(--color-white);
    border-radius: 16px;
    padding: var(--space-6) var(--space-3);
    text-align: center;
    border: 1px solid var(--color-gray-200);
    box-shadow: var(--shadow-sm);
    transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    opacity: 0;
    transform: translateY(20px);
}

.funding-card.animate-fade-in-up {
    opacity: 1;
    transform: translateY(0);
}

.funding-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(255, 122, 47, 0.08) 50%, transparent 100%);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
    z-index: 1;
    pointer-events: none;
}

.funding-card > * {
    position: relative;
    z-index: 2;
}

.funding-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08), 0 0 15px rgba(255, 122, 47, 0.15);
    border-color: var(--color-accent-400);
}

.funding-card:hover::before {
    transform: translateX(100%);
}

.funding-icon {
    width: 70px;
    height: 70px;
    margin: 0 auto var(--space-4);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.35s ease;
    background: var(--color-gray-50);
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
}

.funding-icon i {
    font-size: 1.8rem;
    color: var(--color-primary-800);
    transition: color 0.3s ease;
}

.funding-icon img {
    transition: transform 0.35s ease;
}

.funding-card:hover .funding-icon {
    transform: scale(1.08);
}

.funding-card:hover .funding-icon i {
    color: var(--color-accent-500);
}

.funding-name {
    font-family: var(--font-primary);
    font-weight: 700;
    font-size: var(--font-size-base);
    color: var(--color-primary-900);
    margin-bottom: var(--space-1);
    transition: color 0.3s ease;
}

.funding-card:hover .funding-name {
    color: var(--color-accent-500);
}

.funding-role {
    font-size: 0.75rem;
    color: var(--color-gray-500);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
'''

with open(file_path, 'a', encoding='utf-8') as f:
    f.write(css_content)

print("CSS appended to landing-style.css")

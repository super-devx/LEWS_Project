import re

file_path = r'C:\Users\DELL\OneDrive\Desktop\LEWS_projectt\LEWS_Project\01022021_website\user_entry\login\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove old partners grid
pattern = r'<!-- Partners -->\s*<div class="partners-grid">.*?</div>\s*</div>\s*</div>\s*</div>'
content = re.sub(pattern, '</div>', content, flags=re.DOTALL)

# Insert new funding section before closing container of about section
insert_idx = content.find('</div>\n        </section>\n\n        <!-- CTA Section -->')
if insert_idx == -1:
    print('Could not find insert point')
else:
    new_html = '''
                <!-- Funding Organizations Section -->
                <div class="funding-section mt-5 pt-4">
                    <div class="funding-banner-wrapper text-center mb-5">
                        <div class="funding-line-left"></div>
                        <div class="funding-banner">
                            Funding organizations
                        </div>
                        <div class="funding-line-right"></div>
                    </div>
                    <div class="funding-grid">
                        <div class="funding-card">
                            <div class="funding-icon">
                                <i class="fas fa-building-columns"></i>
                            </div>
                            <div class="funding-name">CSIR-CBRI</div>
                            <div class="funding-role">Research Partner</div>
                        </div>
                        <div class="funding-card">
                            <div class="funding-icon">
                                <i class="fas fa-graduation-cap"></i>
                            </div>
                            <div class="funding-name">IIT Roorkee</div>
                            <div class="funding-role">Technical Partner</div>
                        </div>
                        <div class="funding-card">
                            <div class="funding-icon">
                                <i class="fas fa-leaf"></i>
                            </div>
                            <div class="funding-name">NMHS</div>
                            <div class="funding-role">Funding Agency</div>
                        </div>
                        <div class="funding-card">
                            <div class="funding-icon">
                                <img src="{% static 'images/drdo-logo.png' %}" alt="DRDO" class="img-fluid" style="max-height: 50px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                <div class="fallback-icon" style="display:none; align-items:center; justify-content:center; height:100%;"><i class="fas fa-shield-alt text-primary fs-3"></i></div>
                            </div>
                            <div class="funding-name">DRDO</div>
                            <div class="funding-role">Funding Agency</div>
                        </div>
                        <div class="funding-card">
                            <div class="funding-icon">
                                <img src="{% static 'images/kdisc-logo.png' %}" alt="K-DISC" class="img-fluid" style="max-height: 50px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                <div class="fallback-icon" style="display:none; align-items:center; justify-content:center; height:100%;"><i class="fas fa-lightbulb text-primary fs-3"></i></div>
                            </div>
                            <div class="funding-name">K-DISC</div>
                            <div class="funding-role">Funding Agency</div>
                        </div>
                        <div class="funding-card">
                            <div class="funding-icon">
                                <img src="{% static 'images/isro-logo.png' %}" alt="ISRO" class="img-fluid" style="max-height: 50px;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                <div class="fallback-icon" style="display:none; align-items:center; justify-content:center; height:100%;"><i class="fas fa-satellite text-primary fs-3"></i></div>
                            </div>
                            <div class="funding-name">ISRO</div>
                            <div class="funding-role">Funding Agency</div>
                        </div>
                    </div>
                </div>
            '''
    content = content[:insert_idx] + new_html + content[insert_idx:]

    # Update IntersectionObserver
    content = content.replace("'.feature-card, .partner-card, .about-mission'", "'.feature-card, .partner-card, .about-mission, .funding-banner-wrapper, .funding-card'")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated HTML successfully.')

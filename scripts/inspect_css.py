with open('goalstar-recall/home.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
css_match = re.search(r'<style>(.*?)</style>', text, re.DOTALL)
if css_match:
    css = css_match.group(1)
    print("CSS length:", len(css))
    # print all selectors
    selectors = [m.strip() for m in re.findall(r'([^{]+)\{', css)]
    print("Sample selectors (first 25):")
    for s in selectors[:25]:
        print("  ", s.replace('\n', ' '))
    print(f"Total CSS rule blocks: {len(selectors)}")

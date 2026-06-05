import sys

with open("views.py", "r", encoding="utf-8") as f:
    content = f.read()

part1_search = """      plt.close(fig)
      chart_index += 1
      
    from datetime import datetime
    now = datetime.now()"""

part1_replace = """      plt.close(fig)
      chart_index += 1
      
    # Calculate status level dynamically based on highest graph variance
    status_level = 1
    max_variance = 0
    try:
        import pandas as pd
        for key in keys:
            temp_data = drawlist[key]
            if len(temp_data['y']) > 0:
                raw_y = pd.to_numeric(pd.Series(temp_data['y']), errors='coerce').dropna()
                if len(raw_y) > 0:
                    y_max = raw_y.abs().max()
                    max_variance = max(max_variance, y_max)
        
        if max_variance > 80: status_level = 4
        elif max_variance > 50: status_level = 3
        elif max_variance > 20: status_level = 2
        else: status_level = 1
        
        global graph_danger_level
        graph_danger_level = status_level
    except Exception as e:
        print("Error calculating status level:", e)
        global graph_danger_level
        graph_danger_level = 1

    from datetime import datetime
    now = datetime.now()"""

part2_search = """def monitoring_page(request):
    \"\"\"Render the Monitoring Scale page\"\"\"
    global check, name
    context = {
        'user_name': name if check == "credit" else None,
        # Simulate a graph status level (1-4). This can be updated via a database or API later.
        'graph_status_level': 1
    }
    return render(request, 'monitoring.html', context)"""

part2_replace = """def monitoring_page(request):
    \"\"\"Render the Monitoring Scale page\"\"\"
    global check, name
    global graph_danger_level
    
    try:
        status_level = graph_danger_level
    except NameError:
        status_level = 1
        
    context = {
        'user_name': name if check == "credit" else None,
        'graph_status_level': status_level
    }
    return render(request, 'monitoring.html', context)"""

if part1_search in content and part2_search in content:
    content = content.replace(part1_search, part1_replace)
    content = content.replace(part2_search, part2_replace)
    with open("views.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Strings not found!")
    if part1_search not in content: print("Part 1 missing")
    if part2_search not in content: print("Part 2 missing")

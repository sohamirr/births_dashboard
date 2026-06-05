import matplotlib.pyplot as plt
import seaborn as sns

# Define Spider-Man Inspired Hex Palette
SPIDEY_RED = "#C1121F"
SPIDEY_NAVY = "#003049"
SPIDEY_BLACK = "#111111"
SPIDEY_WHITE = "#FDF0D5"
SPIDEY_GRAY = "#8D99AE"

def apply_spidey_style(fig, ax):
    """Custom helper to strip chart backgrounds and colorize text/axes for the theme"""
    fig.patch.set_alpha(0.0)  # Removes the figure background box completely
    ax.set_facecolor("none")  # Removes individual plot background box
    
    # Force labels, titles, and ticks to be clean white/light gray
    ax.title.set_color(SPIDEY_WHITE)
    ax.xaxis.label.set_color(SPIDEY_GRAY)
    ax.yaxis.label.set_color(SPIDEY_GRAY)
    ax.tick_params(colors=SPIDEY_GRAY, which='both')
    
    # Colorize the surrounding border spikes (spines)
    for spine in ax.spines.values():
        spine.set_color("#333333")
    ax.grid(True, color="#222222", linestyle="--", linewidth=0.5)

# 1. PIE CHART
def plot_pie_chart(df):
    season_data = df.groupby('season')['births'].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Custom color ring wheel mapping
    colors = [SPIDEY_RED, SPIDEY_NAVY, "#4A0E17", SPIDEY_GRAY]
    wedges, texts, autotexts = ax.pie(
        season_data, labels=season_data.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops=dict(color=SPIDEY_WHITE)
    )
    for autotext in autotexts:
        autotext.set_color('white')
        
    ax.set_title("Distribution of Births by Season")
    apply_spidey_style(fig, ax)
    ax.grid(False) # Disable grid overlay line loops for pie charts
    plt.tight_layout()
    return fig

# 2. HISTOGRAM
def plot_histogram(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df, x='births', kde=True, color=SPIDEY_RED, ax=ax, bins=30, line_kws={'linewidth': 2})
    ax.lines[0].set_color(SPIDEY_WHITE) # Make trend line pop out
    ax.set_title("Frequency Distribution of Daily Birth Counts")
    ax.set_xlabel("Births per Day")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 3. BOX PLOT
def plot_box_plot(df):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df, x='day_name', y='births', order=day_order, palette=[SPIDEY_NAVY, SPIDEY_RED], ax=ax)
    ax.set_title("Daily Birth Distribution Grouped by Day of Week")
    ax.set_xlabel("Day of the Week")
    plt.xticks(rotation=15)
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 4. LINE CHART
def plot_line_chart(df):
    yearly_data = df.groupby('year')['births'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(data=yearly_data, x='year', y='births', marker='o', color=SPIDEY_RED, ax=ax, linewidth=2.5, markersize=7)
    ax.set_title("Total Annual US Births Trend")
    ax.locator_params(integer=True)
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 5. BAR CHART
def plot_bar_chart(df):
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly_avg = df.groupby('month_name')['births'].mean().reindex(month_order).reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=monthly_avg, x='month_name', y='births', palette=[SPIDEY_NAVY, SPIDEY_RED], ax=ax)
    ax.set_title("Average Daily Births by Month")
    plt.xticks(rotation=30)
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 6. SCATTER PLOT
def plot_scatter_plot(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x='day_of_year', y='births', alpha=0.4, color=SPIDEY_WHITE, edgecolors=SPIDEY_RED, ax=ax)
    ax.set_title("Daily Birth Counts vs. Day of the Year")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 7. HEATMAP
def plot_heatmap(df):
    numerical_cols = df[['year', 'month', 'date_of_month', 'day_of_week', 'births', 'day_of_year']]
    fig, ax = plt.subplots(figsize=(6, 5))
    # Custom spider-suit gradient map (Black to Navy to Red)
    cmap = sns.diverging_palette(240, 10, n=9, as_cmap=True)
    sns.heatmap(numerical_cols.corr(), annot=True, cmap=cmap, fmt=".2f", ax=ax, cbar=False)
    ax.set_title("Correlation Matrix of Numeric Columns")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 8. AREA CHART
def plot_area_chart(df):
    timeline = df.groupby(['year', 'month'])['births'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(range(len(timeline)), timeline['births'], color=SPIDEY_RED, alpha=0.25)
    ax.plot(range(len(timeline)), timeline['births'], color=SPIDEY_RED, linewidth=1.5)
    ax.set_title("Monthly Total Birth Volume Trend")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 9. COUNT PLOT
def plot_count_plot(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='year', palette=[SPIDEY_NAVY, SPIDEY_RED], ax=ax)
    ax.set_title("Data Record Rows Tracking per Calendar Year")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 10. VIOLIN PLOT
def plot_violin_plot(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.violinplot(data=df, x='season', y='births', palette=[SPIDEY_NAVY, SPIDEY_RED], inner="quartile", ax=ax)
    ax.set_title("Birth Density Profiles Across Seasons")
    apply_spidey_style(fig, ax)
    plt.tight_layout()
    return fig

# 11. BONUS CALENDAR HEATMAP
import matplotlib.colors as mcolors
def plot_calendar_heatmap(df):
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    
    # 1. Build the matrix data grid
    matrix_data = df.pivot_table(values='births', index='month_name', columns='date_of_month', aggfunc='mean')
    matrix_data = matrix_data.reindex(month_order)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 2. CREATE A CUSTOM PALETTE (No Black allowed!)
    # Low values = White/Soft Gray, Mid values = Navy Blue, High values = Deep Spidey Red
    spidey_colors = ["#F4F5F7", "#003049", "#C1121F"]
    
    # FIXED LINE BELOW: Changed 'ColorMapping' to 'Colormap'
    custom_spidey_map = mcolors.LinearSegmentedColormap.from_list("spidey_heatmap", spidey_colors)
    
    # 3. Draw the heatmap with explicit cell borders (linewidths)
    sns.heatmap(
        matrix_data, 
        cmap=custom_spidey_map, 
        annot=False, 
        cbar=True, 
        ax=ax,
        linewidths=0.8,        # Draws clean lines between cells
        linecolor="#1A1D24"    # Soft dark-slate border so cells remain crisp and individual
    )
    
    # 4. Apply titles and text styling
    ax.set_title("Bonus: Calendar Grid Heatmap Matrix (Avg Births by Date & Month)")
    ax.set_xlabel("Day of the Month")
    ax.set_ylabel("Month")
    
    # Run our background remover helper tool
    apply_spidey_style(fig, ax)
    
    # Keep our crisp cell borders visible
    ax.grid(False) 
    
    plt.tight_layout()
    return fig
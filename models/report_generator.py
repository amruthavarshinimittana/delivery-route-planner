import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

CHART_DIR = "static/charts"

class ReportGenerator:
    def __init__(self, routes_data):
        self.df = pd.DataFrame(routes_data) if routes_data else pd.DataFrame()

    def _save(self, fig, filename):
        os.makedirs(CHART_DIR, exist_ok=True)
        path = os.path.join(CHART_DIR, filename)
        fig.savefig(path, bbox_inches='tight', dpi=100, facecolor='#f8f9fa')
        plt.close(fig)
        return filename

    def route_stop_chart(self, stops, distances):
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        colors = ['#2ecc71' if i == 0 else '#3498db' for i in range(len(stops))]
        bars = ax.barh(stops, distances, color=colors, edgecolor='white', height=0.5)
        ax.set_xlabel('Distance from depot (km)', fontsize=11)
        ax.set_title('Optimized delivery route — stop distances', fontsize=13, fontweight='bold', pad=12)
        for bar, val in zip(bars, distances):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{val} km', va='center', fontsize=10, color='#333')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()
        return self._save(fig, "route_stops.png")

    def cost_breakdown_chart(self, fuel_cost, driver_cost):
        fig, ax = plt.subplots(figsize=(5, 4), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        sizes = [fuel_cost, driver_cost]
        labels = [f'Fuel cost\n₹{fuel_cost}', f'Driver cost\n₹{driver_cost}']
        colors = ['#e74c3c', '#3498db']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 10})
        ax.set_title('Cost breakdown', fontsize=13, fontweight='bold', pad=12)
        plt.tight_layout()
        return self._save(fig, "cost_pie.png")

    def history_distance_chart(self):
        if self.df.empty:
            return None
        recent = self.df.tail(8).copy()
        recent['label'] = ['Route ' + str(i+1) for i in range(len(recent))]
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        ax.bar(recent['label'], recent['total_distance'],
               color='#3498db', edgecolor='white', width=0.5)
        ax.set_ylabel('Total distance (km)', fontsize=11)
        ax.set_title('Distance across recent routes', fontsize=13, fontweight='bold', pad=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=20, fontsize=9)
        plt.tight_layout()
        return self._save(fig, "history_distance.png")

    def history_cost_chart(self):
        if self.df.empty:
            return None
        recent = self.df.tail(8).copy()
        labels = ['Route ' + str(i+1) for i in range(len(recent))]
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        ax.plot(labels, recent['total_cost'], marker='o', color='#e74c3c',
                linewidth=2, markersize=7, markerfacecolor='white', markeredgewidth=2)
        ax.fill_between(labels, recent['total_cost'], alpha=0.1, color='#e74c3c')
        ax.set_ylabel('Total cost (₹)', fontsize=11)
        ax.set_title('Delivery cost trend', fontsize=13, fontweight='bold', pad=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=20, fontsize=9)
        plt.tight_layout()
        return self._save(fig, "history_cost.png")
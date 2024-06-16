import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CSVFileForm
from .models import CSVFile
import os

def upload_file(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('analyze_data')
    else:
        form = CSVFileForm()
    return render(request, 'upload.html', {'form': form})

def analyze_data(request):
    try:
        csv_file = CSVFile.objects.latest('uploaded_at')
        file_path = os.path.join(settings.MEDIA_ROOT, csv_file.file.name)
        
        print(f"File path: {file_path}")

        # Read the CSV file
        df = pd.read_csv(file_path)
        
        print(f"DataFrame head: {df.head()}")

        # Perform data analysis
        summary_stats = df.describe()
        first_rows = df.head()
        missing_values = df.isnull().sum().to_frame(name='missing_values')
        
        print(f"Summary stats: {summary_stats}")
        print(f"First rows: {first_rows}")
        print(f"Missing values: {missing_values}")

        # Generate visualizations
        plt.figure(figsize=(10, 6))
        sns.histplot(df.select_dtypes(include=[np.number]).melt(), x='value', hue='variable')
        hist_plot_path = os.path.join(settings.MEDIA_ROOT, 'hist_plot.png')
        plt.savefig(hist_plot_path)
        plt.close()

        context = {
            'summary_stats': summary_stats.to_html(),
            'first_rows': first_rows.to_html(),
            'missing_values': missing_values.to_html(),
            'hist_plot_url': 'media/hist_plot.png',
        }
        return render(request, 'analysis.html', context)
    
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'error.html', {'error': str(e)})
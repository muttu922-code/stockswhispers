from django.contrib.auth import login
from django.shortcuts import render, redirect
import requests
from .forms import SignUpForm

def frontpage(request):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/^NSEI"
    try:
        # Make the API request
        response = requests.get(url)
        
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Try to parse JSON response
            
            # Check if 'chart' key is in the data and extract Nifty value
            if data and 'chart' in data:
                nifty_data = data['chart']['result'][0]['meta']
                nifty_value = nifty_data.get('regularMarketPrice')
            else:
                nifty_value = "Data not available"
        else:
            nifty_value = "Failed to retrieve data. Status code: {}".format(response.status_code)
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        nifty_value = "Error occurred while fetching data: {}".format(str(e))
   
    # Pass Nifty data to template
    return render(request, 'core/frontpage.html', {'nifty_value': nifty_value})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})

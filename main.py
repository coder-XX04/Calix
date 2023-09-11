import wx
import requests
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
CITY_NAME = 'YourCityName'


class HomePage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create a sizer for the home page
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Digital Clock
        self.digital_clock = DigitalClock(self)
        sizer.Add(self.digital_clock, 0, wx.CENTER | wx.ALL, 10)

        # Weather Forecast
        self.weather_label = WeatherLabel(self)
        sizer.Add(self.weather_label, 0, wx.CENTER | wx.ALL, 10)

        self.SetSizerAndFit(sizer)

        # Timer to update the digital clock and weather
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_display, self.timer)
        self.timer.Start(1000)  # Update every second

    def update_display(self, event):
        # Update digital clock
        now = datetime.now()
        time_str = now.strftime("%I:%M:%S %p  ||  %A  ||  %d %B %Y")
        self.digital_clock.SetLabel(time_str)

        # Update weather forecast
        weather_data = self.get_weather_data()
        if weather_data:
            self.weather_label.SetLabel(weather_data)

    def get_weather_data(self):
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            data = response.json()
            if data['cod'] == 200:
                temperature = data['main']['temp']
                description = data['weather'][0]['description']
                return f'Weather: {description.capitalize()}, Temperature: {temperature}°C'
            else:
                return 'Weather data not available'
        except Exception as e:
            print(f'Error fetching weather data: {str(e)}')
            return 'Weather data not available'


class WeatherLabel(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="", style=wx.ALIGN_CENTRE)
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)


class DigitalClock(wx.StaticText):
    def __init__(self, parent):
        wx.StaticText.__init__(self, parent, label="", style=wx.ALIGN_CENTRE)
        font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1000, 600))

        self.sidebar = wx.Panel(self, size=(200, 600))
        self.sidebar.SetBackgroundColour(wx.Colour(50, 50, 50))

        self.content = HomePage(self)
        self.content.SetBackgroundColour(wx.Colour(200, 200, 200))

        # Sidebar options
        options = ["Calendar", "To-Do List", "Alarm", "Timer", "News", "Music"]
        self.sidebar_buttons = []
        for option in options:
            button = wx.Button(self.sidebar, label=option, style=wx.BORDER_NONE)
            self.sidebar_buttons.append(button)

        # Layout
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sidebar, 0, wx.EXPAND)
        self.sizer.Add(self.content, 1, wx.EXPAND)

        self.sidebar.SetSizer(wx.BoxSizer(wx.VERTICAL))  # Vertical sizer for buttons
        for button in self.sidebar_buttons:
            self.sidebar.GetSizer().Add(button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

        self.Centre()
        self.Show(True)


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1, 'Calix App')
    app.MainLoop()

from visautils import load_data, plot_data
import matplotlib.pyplot as plt

url = "https://usa.visa.com/content/dam/VCOM/regional/na/us/partner-with-us/economic-insights/documents/vbei-visa-us-smi-data-appendix.xlsx"

plot_data(load_data(url))

plt.savefig("Python/Scrapers/Visa/VisaSpending.png")

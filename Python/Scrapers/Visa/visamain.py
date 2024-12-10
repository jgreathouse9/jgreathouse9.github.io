from visautils import load_data, plot_data

url = "https://usa.visa.com/content/dam/VCOM/regional/na/us/partner-with-us/economic-insights/documents/vbei-visa-us-smi-data-appendix.xlsx"

plot_data(load_data(url))

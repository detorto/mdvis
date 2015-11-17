from filters import RegionFilter

def region_filter(container, region):
	f = RegionFilter(region)
	return f(container)
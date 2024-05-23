---
title: Services Offered
layout: archive
permalink: /consulting/
author_profile: true
---

<div id="London" class="tabcontent">
  <h1>London</h1>
  <p>London is the capital city of England.</p>
</div>

<button class="tablink" onclick="openCity('London', this, 'red')" id="defaultOpen">London</button>

.tablink {
  background-color: #555;
  color: white;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  font-size: 17px;
  width: 25%;
}

/* Change background color of buttons on hover */
.tablink:hover {
  background-color: #777;
}

/* Set default styles for tab content */
.tabcontent {
  color: white;
  display: none;
  padding: 50px;
  text-align: center;
}

/* Style each tab content individually */
#London {background-color:red;}

function openCity(cityName, elmnt, color) {
  // Hide all elements with class="tabcontent" by default */
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove the background color of all tablinks/buttons
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }

  // Show the specific tab content
  document.getElementById(cityName).style.display = "block";

  // Add the specific color to the button used to open the tab content
  elmnt.style.backgroundColor = color;
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();


# Data Management

In research, data must be cleaned before it may be analyzed. However, sometimes this task is more daunting than it appears at first. Often, multiple merges, reshapings, and validation checks must be done to ensure a dataset is ready for analysis. Particularly in an era where data are unstructured (found on webpages, and must be scraped from the internet), efficient, reproducible data management is critical to the success of a project before any analysis is done. If you need to clean data for a project and need a streamlined, efficient way of doing so, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> and we can discuss the details.

# Program Evaluation

Frequently, researchers need to know if some intervention (say, a tax, an anti-tobacco policy, an abortion ban, or some new marketing strategy) had some effect on outcomes that we care about. However, policy is never self justifying; it must be studied and evaluated to see if it actually *achieves* the aims it is meant to achieve. In fact, this goes beyond public policy: sometimes, the interventions we care about ([say](https://static1.squarespace.com/static/5e0fdcef27e0945c43fab131/t/61eb4615e7feef09dcbe7d29/1642808862058/The+Economic+Impact+of+Migrants+from+Hurricane+Maria.pdf), how hurricanes affect economic outcomes) are natural events, more or less, and we wish to understand how these interventions influence outcomes. The gold standard to do this is typically conducting a randomized controlled trial, but this is rarely possible in real life for a host of reasons. Furthermore, we know that simple regression analysis, *even when we adjust for a host of covariates*, rarely provides good causal evidence for real-life treatment effect estimation. Instead, proper program evaluation demands a mixture of domain expertise and judicious application of modern econometric methods. I have experience in causal inference and have packaged numerious such methods in [Python](https://github.com/jgreathouse9/mlsynth) and [Stata](https://ideas.repec.org/c/boc/bocode/s459107.html). If you wish to implement a program evaluation using rigorous and objective methods, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> today for a free consultation so we can discuss your needs.

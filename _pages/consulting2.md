---
title: Services
layout: archive
permalink: /consulting/
author_profile: true
---

Learn more about the services I offer below!

<div id="container">
  <div id="sideMenu">
    <ul>
      <li><a href="#" id="dataManagement">Data Management</a></li>
      <li><a href="#" id="programEvaluation">Program Evaluation</a></li>
    </ul>
  </div>
  <div id="content">
    <!-- The content will be displayed here -->
  </div>
</div>

<style>
  #container {
    display: flex;
  }

  #sideMenu {
    width: 200px;
    margin-right: 20px;
  }

  #sideMenu ul {
    list-style-type: none;
    padding: 0;
  }

  #sideMenu li {
    margin-bottom: 10px;
  }

  #sideMenu a {
    text-decoration: none;
    color: #007bff;
    font-weight: bold;
    cursor: pointer;
  }

  #sideMenu a:hover {
    color: #0056b3;
  }

  #content {
    flex-grow: 1;
    text-align: justify;
  }
</style>

<script>
  document.getElementById('dataManagement').addEventListener('click', function() {
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = `
      In research, data must be cleaned before it may be analyzed. However, sometimes this task is more daunting than it appears at first. 
      Often, multiple merges, reshapings, and validation checks must be done to ensure a dataset is ready for analysis. Particularly in an 
      era where data are unstructured (found on webpages, and must be scraped from the internet), efficient, reproducible data management is 
      critical to the success of a project before any analysis is done. If you need to clean data for a project and need a streamlined, 
      efficient way of doing so, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> and we can discuss the details.
    `;
  });

  document.getElementById('programEvaluation').addEventListener('click', function() {
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = `
      Frequently, researchers need to know if some intervention (say, a tax, an anti-tobacco policy, an abortion ban, or some new 
      marketing strategy) had some effect on outcomes that we care about. However, policy is never self-justifying; it must be 
      studied and evaluated to see if it actually *achieves* the aims it is meant to achieve. In fact, this goes beyond public 
      policy: sometimes, the interventions we care about (<a href="https://static1.squarespace.com/static/5e0fdcef27e0945c43fab131/t/61eb4615e7feef09dcbe7d29/1642808862058/The+Economic+Impact+of+Migrants+from+Hurricane+Maria.pdf">say</a>, 
      how hurricanes affect economic outcomes) are natural events, more or less, and we wish to understand how these interventions influence 
      outcomes. The gold standard to do this is typically conducting a randomized controlled trial, but this is rarely possible in real life 
      for a host of reasons. Furthermore, we know that simple regression analysis, *even when we adjust for a host of covariates*, rarely 
      provides good causal evidence for real-life treatment effect estimation. Instead, proper program evaluation demands a mixture of domain 
      expertise and judicious application of modern econometric methods. I have experience in causal inference and have packaged numerous 
      such methods in <a href="https://github.com/jgreathouse9/mlsynth">Python</a> and <a href="https://ideas.repec.org/c/boc/bocode/s459107.html">Stata</a>. 
      If you wish to implement a program evaluation using rigorous and objective methods, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> today 
      for a free consultation so we can discuss your needs.
    `;
  });
</script>

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
      <li><a href="#" id="faq">FAQ</a></li>
      <li><a href="#" id="dataManagement">Data Management</a></li>
      <li><a href="#" id="programEvaluation">Program Evaluation</a></li>
      <li><a href="#" id="processAutomation">Process Automation</a></li>
      <li><a href="#" id="webScraping">Web Scraping</a></li>
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
  document.addEventListener('DOMContentLoaded', function () {
    // FAQ Section
    document.getElementById('faq').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Frequently Asked Questions (FAQ)</h2>
        <ul>
          <li><strong>What services count as "consulting" versus "not consulting"?</strong> 
            Any large-scale project (i.e., a paper) that I am expected to contribute meaningfully to yet will not be given authorship counts as consulting. 
            For example, if you need to clean and debug a large do file in Stata or implement some synthetic control method, this goes beyond simply talking 
            since I'm expected to make meaningful contributions to the code of the research process. </li>
          <li><strong>Are there differential fees?</strong> 
            Yes, fees depend on who is asking. PHD/grad students have one set of fees and professionals (i.e., professors and people in industry) have a separate tier.</li>
          <li><strong>Are there expedited fees?</strong> 
            Projects where results are expected within one week from the initial consultation are classified as expedited. Expedited fees are the standard hourly 
            fee plus half, no exceptions.</li>
          <li><strong>Is the first consultation free?</strong> 
            Yes, the first 30-minute consultation is free to discuss your project and goals.</li>
        </ul>
      `;
    });

    // Data Management Section
    document.getElementById('dataManagement').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Data Management</h2>
        <p>
          In research, data must be cleaned before it may be analyzed. However, sometimes this task is more daunting than it appears at first. 
          Often, multiple merges, reshapings, and validation checks must be done to ensure a dataset is ready for analysis. Particularly in an 
          era where data are unstructured (found on webpages, and must be scraped from the internet), efficient, reproducible data management is 
          critical to the success of a project before any analysis is done. If you need to clean data for a project and need a streamlined, 
          efficient way of doing so, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> and we can discuss the details.
        </p>
      `;
    });

    // Program Evaluation Section
    document.getElementById('programEvaluation').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Program Evaluation</h2>
        <p>
          Frequently, researchers need to know if some intervention (say, a tax, an anti-tobacco policy, an abortion ban, or some new 
          marketing strategy) had some effect on outcomes that we care about. However, policy is never self-justifying; it must be 
          studied and evaluated to see if it actually achieves the aims it is meant to achieve. 
          If you wish to implement a program evaluation using rigorous and objective methods, 
          <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> today for a free consultation so we can discuss your needs.
        </p>
      `;
    });

    // Process Automation Section
    document.getElementById('processAutomation').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Process Automation</h2>
        <p>
          Automation of workflows saves time, reduces errors, and ensures that tasks once required to be done by people can be done automatically. Whether you need to automate data collection from a web source, the cleaning of manually updated datasets, file organization, or reporting, I can help streamline your processes with GitHub Actions. 
          <a href="mailto:j.greathouse3@student.gsu.edu">Reach out to discuss</a> how automation can help your business or your research purposes.
        </p>
      `;
    });

    // Web Scraping Section
    document.getElementById('webScraping').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Web Scraping</h2>
        <p>
          Extracting data from the web allows you to harness valuable information for research. However, this requires specialized tools and can be tedious if done by hand. I specialize in developing efficient, scalable scraping solutions using Python and GitHub Actions to gather the data you need from websites, APIs, and other online sources. 
          <a href="mailto:j.greathouse3@student.gsu.edu">Contact me</a> to learn more about how I can help with your web scraping needs.
        </p>
      `;
    });
  });
</script>

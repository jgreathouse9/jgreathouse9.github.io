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
    document.getElementById('faq').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `<h2>FAQ</h2><p>FAQ content loaded successfully!</p>`;
    });

    document.getElementById('dataManagement').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `<h2>Data Management</h2>
      <p>
        In research, data must be cleaned before it may be analyzed. However, sometimes this task is more daunting than it appears at first. 
        Often, multiple merges, reshapings, and validation checks must be done to ensure a dataset is ready for analysis. Particularly in an 
        era where data are unstructured (found on webpages, and must be scraped from the internet), efficient, reproducible data management is 
        critical to the success of a project before any analysis is done. If you need to clean data for a project and need a streamlined, 
        efficient way of doing so, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> and we can discuss the details.
      </p>`;
    });
  });
</script>

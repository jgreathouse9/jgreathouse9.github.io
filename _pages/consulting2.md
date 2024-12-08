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
      <li><a href="#" id="webScraping">Web Scraping</a></li>
      <li><a href="#" id="processAutomation">Process Automation</a></li>
      <li><a href="#" id="contact">Contact</a></li>
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
  contentDiv.innerHTML = `
    <h2>FAQ</h2>
    <p>Here you can find answers to frequently asked questions about my services.</p>
    <ul>
      <li><strong>What services count as "consulting" versus "not consulting"?</strong>
        Any large-scale project (i.e., a paper) that I am 1) expected to contribute meaningfully to yet 2) will not be given authorship for/intellectual property rights over counts as consulting. For example, if you need to clean and debug a large do file in Stata for some analysis or implement some monthly web scraping method, this counts since I'm expected to make meaningful contributions to the code and flow of the research process.</li>
      <li><strong>Are there differential fees?</strong>
        Fees depend on who is reaching out to me. PHD/grad students have one set of fees. Professionals (i.e., professors and people in the industry) and businesses have a separate set of fees.</li>
      <li><strong>Are there expedited fees?</strong>
        Yes. Projects where results are expected within one week from the initial consultation are classified as expedited. Expedited billing is time and a half, <strong>no exceptions</strong>.</li>
      <li><strong>Is the first consultation free?</strong>
        Yes, the first 30-minute consultation is free. In your introduction email to me, simply reach out and tell me what you would like for me to work on in enough detail, and when we first meet we will discuss the finer points. </li>
    </ul>
  `;
});



    document.getElementById('dataManagement').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Data Management</h2>
        <p>
          In research, data must be cleaned before it may be analyzed. However, sometimes this task is more daunting than it appears at first. 
          Often, multiple merges, reshapings, and validation checks must be done to ensure a dataset is ready for analysis. If you need to clean data for a project and need a streamlined, 
          efficient way of doing so, <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> and we can discuss the details.
        </p>
      `;
    });

    document.getElementById('programEvaluation').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Program Evaluation</h2>
        <p>
          Frequently, researchers need to know if some intervention (say, a tax, an anti-tobacco policy, an abortion ban, or some new 
          marketing strategy) had some effect on outcomes that we care about. However, policy is never self-justifying; it must be 
          studied and evaluated to see if it actually <strong>achieves</strong> the aims it is meant to achieve. In fact, this goes beyond public 
          policy: sometimes, the interventions we care about (<a href="https://static1.squarespace.com/static/5e0fdcef27e0945c43fab131/t/61eb4615e7feef09dcbe7d29/1642808862058/The+Economic+Impact+of+Migrants+from+Hurricane+Maria.pdf">say</a>, 
          how hurricanes affect economic outcomes) are natural events, more or less, and we wish to understand how these interventions influence 
          outcomes. If you wish to implement a program evaluation using rigorous and objective methods, 
          <a href="mailto:j.greathouse3@student.gsu.edu">contact me</a> today for a free consultation so we can discuss your needs.
        </p>
      `;
    });

    document.getElementById('webScraping').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Web Scraping</h2>
        <p>
          Unstructured data present academics and businesses with a wealth of data at their fingertips. However, unstructured data is in principle difficult (in many cases) to collect because it involves web scraping, or the gathering of data from websites, latent APIs, or HTML source code. 
          I can design custom web scraping tools that are efficient and scalable, often integrated into a GitHub Action to allow for fully automated data collection. <a href="mailto:j.greathouse3@student.gsu.edu">Contact me</a> 
          to discuss how web scraping can be utilized for your specific project needs.
        </p>
      `;
    });

    document.getElementById('processAutomation').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Process Automation</h2>
        <p>
          Automation is key to optimizing workflows and saving time on repetitive tasks. I can help you automate a wide variety of processes, 
          from data extraction and cleaning to reporting and visualization of data. Whether it's setting up automated data pipelines or integrating APIs 
          to grab real-time data, automation ensures that human labor can be devoted to something more worthwhile. If you want to 
          streamline your data operations, <a href="mailto:j.greathouse3@student.gsu.edu">reach out</a> and we can discuss your needs in detail.
        </p>
      `;
    });

    document.getElementById('contact').addEventListener('click', function () {
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = `
        <h2>Contact</h2>
        <p>
          If you'd like to learn more about my services or discuss your project needs, <a href="mailto:j.greathouse3@student.gsu.edu">email me</a> directly, and I'll get back to you.
        </p>
      `;
    });
  });
</script>

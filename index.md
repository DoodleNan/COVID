---
layout: default
title: COVID-19 Outbreak in Luxembourg
comments: true
---

<script>
  function resizeIframeh(obj) {
    obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';
  }
</script>

<div id="date"  style="width:100%; height:25px; float:left;">
<iframe src="./subpage_date_luxembourg.html"
    sandbox="allow-same-origin allow-scripts"
    scrolling="no"
    height="30px"
    seamless="seamless"
    frameborder="0"></iframe>
</div>
<div id="resume"  style="width:100%; height:25px; overflow:hidden; text-align:center;">
<div id="confirmed"  style="width: 120px; float:left;">
<iframe src="./subpage_confirmed_luxembourg.html"
    sandbox="allow-same-origin allow-scripts"
    scrolling="no"
    height="25px"
    seamless="seamless"
    frameborder="0"></iframe>
</div>
<div id="recovered" style="width: 94px; float:left;">
<iframe src="./subpage_recovered_luxembourg.html"
    sandbox="allow-same-origin allow-scripts"
    scrolling="no"
    height="25px"
    seamless="seamless"
    frameborder="0"></iframe>
</div>
<div id="died" style="width:30px; float:left;">
<iframe src="./subpage_died_luxembourg.html"
    sandbox="allow-same-origin allow-scripts"
    scrolling="no"
    height="25px"
    seamless="seamless"
    frameborder="0"></iframe>
</div>
</div>

<iframe src="./plot.html"
    sandbox="allow-same-origin allow-scripts"
    height="365px"
    width="100%"
    scrolling="no"
    seamless="seamless"
    frameborder="0">
</iframe>

### Source:

- English:
	- [The Luxembourg Government](https://www.gouvernement.lu/coronavirus)
	- [RTL Today](https://today.rtl.lu/news/luxembourg)
	- [RTL LIVE TICKER](https://today.rtl.lu/news/luxembourg/a/1481968.html)

### Worldwide Tracker:

- [worldometers](https://www.worldometers.info/coronavirus/)
- [Roylab Stats](https://www.youtube.com/watch?v=qgylp3Td1Bw)
- [JOHNS HOPKINS UNIVERSITY](https://coronavirus.jhu.edu/map.html)

### To-Do:

- Active Patient Plot: Confirmed - (recovered + dead) case

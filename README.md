<h1 align="center"> 
Hello World Inference Extension v1.0.0
</h1>

## Table of Contents

- [About](#about)
- [For More](#for-more)

## About 

This extension is a part of the [Hello World Template](https://github.com/AhmedCoolProjects/sonic_engine_templates/tree/main/hello_world) as a **inference** extension.

It is a tiny extension that uses [VirusTotal API](https://developers.virustotal.com/reference/overview) to request a complete analysis and predictions for **src_ip** addresses extracted by [Hello World Feature Extension](https://github.com/AhmedCoolProjects/hello_world_feature_extension_sonic_engine).
After each response, the extension publish an object includes an `id`, `timestamp`, the `data`, `result` and the requested `url` into another redis channel to provide this object for other extensions that may use it.

## For More 

- [Sonic Engine Extensions API](https://github.com/sooualil/sonic_engine_yapsy/tree/as-package#extensions-api)
- [Sonic Engine Repo](https://github.com/sooualil/sonic_engine_yapsy/tree/as-package#readme)
- [Sonic Engine Templates](https://github.com/AhmedCoolProjects/sonic_engine_templates/tree/main)
- [Hello World Feature Extension](https://github.com/AhmedCoolProjects/hello_world_feature_extension_sonic_engine)
- [Hello World Reporting Extension](https://github.com/AhmedCoolProjects/hello_world_reporting_extension)

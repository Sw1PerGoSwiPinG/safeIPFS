<template>
    <!-- Place the component inside a div with a given width -->
    <div class="everyday-container">
        <div style="height: 30px;"></div>
        <div class="everyday">
            <VueUiHeatmap :dataset="dataset" :config="config" />
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { VueUiHeatmap } from "vue-data-ui";
import "vue-data-ui/style.css";

const config = ref({
    "style": {
        "backgroundColor": "#FFFFFF",
        "color": "#CCCCCC",
        "fontFamily": "inherit",
        "layout": {
            "useDiv": true,
            "padding": {
                "top": 36, "right": 6, "bottom": 0, "left": 40
            },
            "cells": {
                "height": 28,
                "value": {
                    "show": true, "fontSize": 10, "bold": false, "roundingValue": 0, "color": "#CCCCCC"
                }, 
                "colors": { 
                    "hot": "#ff6400", "cold": "#5f8bee", "underlayer": "#1A1A1A" 
                }, 
                "spacing": 0.5, 
                "selected": { 
                    "border": 2, "color": "#2D353C" 
                }
            }, 
            "dataLabels": { 
                "xAxis": { 
                    "show": true, 
                    "values": ["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10", "w11", "w12", "w13", "w14", "w15", "w16", "w17", "w18", "w19", "w20", "w21", "w22", "w23", "w24", "w25", "w26", "w27", "w28", "w29", "w30", "w31", "w32", "w33", "w34", "w35", "w36", "w37", "w38", "w39", "w40"], 
                    "fontSize": 8, 
                    "color": "#000000",
                    "bold": false, 
                    "offsetX": 0, 
                    "offsetY": 0 
                }, 
                "yAxis": { 
                    "show": true, 
                    "values": [], 
                    "fontSize": 8, 
                    "color": "#000000", 
                    "bold": false, 
                    "offsetY": 0, 
                    "offsetX": 0 
                } 
            }
        }, 
        "title": { 
            "text": "SafeIPFS系统2023年每日上传数据量（单位GiB）", 
            "color": "#000000", 
            "fontSize": 18, 
            "bold": false 
        }, 
        "legend": { 
            "show": true, 
            "backgroundColor": "#2A2A2A", 
            "color": "#000000", 
            "fontSize": 8, 
            "bold": true, 
            "roundingValue": 0 
        }, 
        "tooltip": { 
            "show": true, 
            "backgroundColor": "#2A2A2A", 
            "color": "#CCCCCC", 
            "fontSize": 14, 
            "roundingValue": 0 
        }
    }, 
    "table": { 
        "show": false, 
        "responsiveBreakpoint": 400, 
        "th": { 
            "backgroundColor": "#B7EB8F", 
            "color": "#38B90D", 
            "outline": "none" 
        }, 
        "td": { 
            "backgroundColor": "#F6FFED", 
            "color": "#38B90D", 
            "outline": "none", 
            "roundingValue": 1, 
            "roundingPercentage": 0
        } 
    }, 
    "userOptions": { "show": true }
});

const dataset = ref([
    { 
        "name": "Sun", 
        "values": [4.5, 2.2, 3.8, 7.8, 8.8, 7, 11.2, 4, 4.4, 8.5, 7, 12.2, 4, 7.1, 12.5, 13.6, 11, 16.1, 21, 18.6, 11.8, 18.8, 17.5, 21.6, 16.6, 18, 25.2, 24, 24, 22.6, 21.4, 21.6, 21, 21.5, 22.1, 16.6, 13, 13.9, 15.2, 11.4] 
    }, 
    { 
        "name": "Mon", 
        "values": [2.8, 5, 1.4, 6.1, 6.6, 8.6, 7.9, 3.8, 2.5, 8.7, 11.5, 12.3, 5.2, 11.5, 12.6, 12.1, 13.3, 17.6, 21, 16.6, 13, 16.6, 16.8, 18, 17.4, 18.2, 22.8, 18.2, 22.3, 22, 21.8, 21.8, 21.4, 22.5, 22, 19.7, 13, 12.7, 12.3, 14.4] 
    }, 
    { 
        "name": "Tue", 
        "values": [8.1, 4, 0, 6.8, 8.1, 7.3, 8.8, 5.8, 4.9, 9.8, 11.8, 11.4, 11.3, 14.6, 12.1, 11.6, 14.1, 20, 22.3, 13.5, 15.4, 17.7, 19, 19.5, 18.7, 18.4, 24.8, 18.3, 19.1, 23.5, 23.7, 21.6, 23.1, 21, 21.6, 21.9, 12.6, 11.7, 13.1, 12.3] 
    }, 
    { 
        "name": "Wed", 
        "values": [1, 4.8, 1.3, 9.5, 5.7, 12.2, 7.9, 6.5, 8.3, 11.8, 9.9, 11.2, 10, 13.2, 12.7, 12.2, 13.1, 18.8, 22.4, 15.1, 15.2, 16.7, 22, 19.6, 18.9, 19, 27, 21, 19.7, 26.9, 25.7, 21.6, 24.7, 21.6, 18.3, 21.8, 12.9, 11.8, 16.4, 12.4] 
    }, 
    { 
        "name": "Thu", 
        "values": [2.2, 3.5, 4.4, 6.7, 7, 11.3, 7.8, 8.2, 9.5, 8.5, 11.9, 5.3, 11.3, 13.9, 13, 14.5, 13.7, 16, 21.4, 16.5, 17.6, 16.1, 22.4, 21.6, 15.2, 18.8, 24.3, 21.2, 21.6, 23.4, 25.6, 21.1, 23.4, 22.2, 17.8, 18.4, 13.1, 11.1, 13.9, 14] 
    }, 
    { 
        "name": "Fri", 
        "values": [1.1, 2.8, 5.4, 6.9, 3.3, 9.9, 5.2, 8.1, 10, 8.4, 11.4, 2.5, 6, 14, 14, 13.8, 15.4, 15, 17.1, 15.5, 18.1, 18.3, 25.1, 19.9, 16.1, 18.8, 21.1, 21.4, 22.4, 21.5, 25.7, 21, 21.4, 19.9, 17.1, 14.4, 14.7, 12.2, 12.2, 15.4] 
    }, 
    { 
        "name": "Sat", 
        "values": [6.1, 1, 4.3, 8.6, 5.8, 2.5, 6.6, 3.7, 6.9, 8.4, 11.1, 11.6, 3.5, 5.6, 12.8, 13.6, 11.2, 15.2, 16.5, 17.2, 14.5, 21.2, 19.4, 18.3, 16.5, 18.5, 21.5, 22.1, 21.3, 23.8, 18.7, 25.2, 18.8, 21.2, 19.2, 16.3, 11.9, 14.2, 16.5, 12.6] 
    }
]);
</script>

<style scoped>
.everyday-container {
    width: 80%;
    margin-left: 10%;
    background-color: white;
	border-radius: 10px;
	box-sizing: border-box;
}

.everyday {
    margin-bottom: 20px;
}
</style>
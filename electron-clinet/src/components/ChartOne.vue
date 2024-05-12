<template>
    <div class="chart-container">
        <div class="chart-title">
            <label><input type="radio" name="chartType" value="line" v-model="chartType">今日流量趋势</label>
            <label><input type="radio" name="chartType" value="bar" v-model="chartType">本月访问量</label>
        </div>
        <canvas ref="chartCanvas"></canvas>        
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
    setup() {
        const chartType = ref('line');
        const chartCanvas = ref(null);
        let chartInstance = null;

        const createChart = () => {
            const ctx = chartCanvas.value.getContext('2d');

            if (chartInstance) {
                chartInstance.destroy();
            }

            chartInstance = new Chart(ctx, {
                type: chartType.value,
                data: {
                    labels: chartType.value === 'line' ? ['6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'] :
                        ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
                    datasets: [{
                        label: chartType.value === 'line' ? '流量' : '访问量',
                        data: chartType.value === 'line' ? [15000, 48000, 45000, 25000, 28000, 32000, 40000, 30000, 15000, 44000, 46000, 48000, 18000, 35000, 38000, 22000, 42000, 49000] :
                            [3000, 4000, 6500, 7500, 4500, 6500, 7000, 5500, 6000, 8000, 3000, 5000],
                        backgroundColor: chartType.value === 'line' ? 'rgba(54, 162, 235, 0.2)' : 'rgba(255, 99, 132, 0.2)', // 填充颜色
                        borderColor: chartType.value === 'line' ? 'rgba(54, 162, 235, 1)' : 'rgba(255, 99, 132, 1)', // 边框颜色
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        };

        onMounted(() => {
            createChart();
        });

        watch(chartType, () => {
            createChart();
        });

        return {
            chartType,
            chartCanvas
        };
    }
};
</script>

<style scoped>
.chart-container {
    width: 80%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;

    background-color: white;
	/* border: 1px solid #000; 显示边框 */
	border-radius: 10px;
	/* 圆角矩形 */
	padding: 30px;
	box-sizing: border-box;
	/* 边框包含在盒子内 */
}

.chart-title {
    flex: 1;
    text-align: center;
    font-size: 18px;
    margin-bottom: 10px;
}

/* .chart-canvas {
    width: 100%;
    height: 500px;
} */
</style>
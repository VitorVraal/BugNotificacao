import { ref, onMounted, onUnmounted } from "vue";

export function useDashboard() {
  const dashboardStats = ref({
    totalProducts: 0,
    lowStockProducts: 0,
    pendingDeliveries: 0,
    productOutput: 0,
    totalProductsTrend: "",
    lowStockProductsTrend: "",
    pendingDeliveriesTrend: "",
    productOutputTrend: "",
  });

const fetchDashboardStats = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/dashboard/stats");
    const data = await response.json();

    if (!response.ok || data.success === false || !data.data) {
      console.error("Erro no backend:", data.message || "Resposta inesperada do servidor");
      return;
    }


    updateStats(data.data);
  } catch (error) {
    console.error("Erro na requisição:", error);
  }
};





  const updateStats = (response) => {
    const stats = response.data || response;

    if (!stats) {
      console.error("Dados de estatística ausentes");
      return;
    }

    dashboardStats.value = {
      totalProducts: stats.total_produtos || 0,
      lowStockProducts: stats.produtos_baixo_estoque || 0,
      productOutput: stats.saida_produtos || 0,
      totalProductsTrend: stats.total_produtos_trend || "",
      lowStockProductsTrend: stats.produtos_baixo_estoque_trend || "",
      pendingDeliveriesTrend: stats.entregas_pendentes_trend || "",
      productOutputTrend: stats.saida_produtos_trend || ""
    };
  };


  // Conexão WebSocket para atualização em tempo real WebSocket
  let ws = null;

  const initializeWebSocket = () => {
  ws = new WebSocket("ws://localhost:8000/ws/dashboard");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "DASHBOARD_STATS_UPDATE" && data.data) {
        updateStats({ success: true, data: data.data });
      }
    };

    ws.onclose = () => {
      // Tenta reconectar após 5 segundos
      setTimeout(initializeWebSocket, 5000);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  };

  onMounted(() => {
    fetchDashboardStats();
    initializeWebSocket();
  });

  onUnmounted(() => {
    if (ws) ws.close();
  });

  return {
    dashboardStats,
    fetchDashboardStats,
  };
}
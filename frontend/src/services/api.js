import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Funções específicas para estoque
export const estoqueApi = {
  async getProdutos() {
    try {
      const response = await api.get('/produto');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
      throw error;
    }
  },

  async getStockStats() {
    try {
      const produtos = await this.getProdutos();
      
      // Calcular estatísticas
      const totalProducts = produtos.length;
      const lowStockCount = produtos.filter(p => p.qtde_estoque < p.qtd_minima_produto).length;
      
      return {
        totalProducts,
        lowStockCount,
        updateCount: 0 // Você pode implementar isso depois
      };
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error);
      throw error;
    }
  },

async updateProduto(data) {
  try {
    console.log("Enviando dados para atualização:", data);
    const response = await api.put('/produto', data, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Erro detalhado ao atualizar produto:', {
      error: error.response?.data,
      status: error.response?.status,
      config: error.config
    });
    throw error;
  }
},

async deleteProduto(id) {
  try {
    console.log(`Enviando requisição DELETE para /produto/${id}`);
    const response = await api.delete(`/produto/${id}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar produto:', {
      error: error.response?.data,
      status: error.response?.status,
      config: error.config
    });
    throw error;
  }
}
};

export default api;
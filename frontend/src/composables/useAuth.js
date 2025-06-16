import { ref } from "vue";
import api from "@/services/api"; // axios

const user = ref(null);
const isAuthenticated = ref(false);
const isLoading = ref(false);
const error = ref(null);

const register = async (email, senha) => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.post("/usuarios", {
      email_usuario: email,
      senha_usuario: senha
    });

    return response.data;
  } catch (e) {
    error.value = e.response?.data?.detail || "Erro ao cadastrar";
    throw e;
  } finally {
    isLoading.value = false;
  }
};


const loadStoredAuth = () => {
  const storedUser = localStorage.getItem("user");
  const storedToken = localStorage.getItem("token");
  if (storedUser && storedToken) {
    user.value = JSON.parse(storedUser);
    isAuthenticated.value = true;
    api.defaults.headers.common["Authorization"] = `Bearer ${storedToken}`;
  }
};

loadStoredAuth();

export function useAuth() {
  const login = async (email, password) => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.post("/login", {
      email_usuario: email,
      senha_usuario: password,
    });

    const { access_token } = response.data;

    localStorage.setItem("token", access_token);
    api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

    // Se quiser pegar o payload do token para setar o user, pode decodificar aqui:
    const payload = JSON.parse(atob(access_token.split('.')[1]));
    user.value = { id: payload.id, email: payload.email };

    isAuthenticated.value = true;
    return true;
  } catch (e) {
    error.value = e.response?.data?.detail || "Erro no login";
    throw new Error(error.value);
  } finally {
    isLoading.value = false;
  }
};


  const logout = () => {
    user.value = null;
    isAuthenticated.value = false;
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    register,
  };
}

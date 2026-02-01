// lib/services/auth_service.dart
// Servicio de autenticación

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../utils/constants.dart';

class AuthService extends ChangeNotifier {
  User? _user;
  String? _token;
  bool _isLoading = false;

  User? get user => _user;
  String? get token => _token;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _token != null;

  // ==========================================================================
  // INICIALIZAR - Cargar token guardado
  // ==========================================================================
  
  Future<bool> initialize() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
    
    if (_token != null) {
      // Verificar si el token sigue siendo válido
      final success = await getProfile();
      if (!success) {
        await logout();
        return false;
      }
      return true;
    }
    return false;
  }

  // ==========================================================================
  // LOGIN
  // ==========================================================================
  
  Future<Map<String, dynamic>> login(String email, String password) async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.login}'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': email,
          'password': password,
        },
      );

      _isLoading = false;
      notifyListeners();

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _token = data['access_token'];
        
        // Guardar token
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', _token!);
        
        // Obtener perfil del usuario
        await getProfile();
        
        return {'success': true};
      } else {
        final error = json.decode(response.body);
        return {'success': false, 'message': error['detail'] ?? 'Error al iniciar sesión'};
      }
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return {'success': false, 'message': 'Error de conexión. Verifica tu internet.'};
    }
  }

  // ==========================================================================
  // REGISTRO
  // ==========================================================================
  
  Future<Map<String, dynamic>> register(String email, String password, String? fullName, String? phone) async {
    _isLoading = true;
    notifyListeners();

    try {
      final body = {
        'email': email,
        'password': password,
      };
      
      if (fullName != null && fullName.isNotEmpty) {
        body['full_name'] = fullName;
      }
      if (phone != null && phone.isNotEmpty) {
        body['phone'] = phone;
      }

      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.register}'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(body),
      );

      _isLoading = false;
      notifyListeners();

      if (response.statusCode == 201) {
        return {'success': true};
      } else {
        final error = json.decode(response.body);
        return {'success': false, 'message': error['detail'] ?? 'Error al registrarse'};
      }
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      return {'success': false, 'message': 'Error de conexión. Verifica tu internet.'};
    }
  }

  // ==========================================================================
  // OBTENER PERFIL
  // ==========================================================================
  
  Future<bool> getProfile() async {
    if (_token == null) return false;

    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.userMe}'),
        headers: {
          'Authorization': 'Bearer $_token',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _user = User.fromJson(data);
        notifyListeners();
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  // ==========================================================================
  // LOGOUT
  // ==========================================================================
  
  Future<void> logout() async {
    _token = null;
    _user = null;
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    
    notifyListeners();
  }
}
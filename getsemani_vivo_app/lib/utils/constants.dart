// lib/utils/constants.dart
// Constantes de la aplicación Getsemaní Vivo

import 'package:flutter/material.dart';

// =============================================================================
// COLORES DE LA APP
// =============================================================================

class AppColors {
  // Colores principales
  static const Color primary = Color(0xFF1A5276);      // Azul oscuro
  static const Color secondary = Color(0xFFE74C3C);    // Rojo coral
  static const Color accent = Color(0xFFF39C12);       // Naranja/dorado
  
  // Fondos
  static const Color background = Color(0xFFF5F6FA);   // Gris muy claro
  static const Color white = Colors.white;
  static const Color black = Color(0xFF2C3E50);
  
  // Estados
  static const Color success = Color(0xFF27AE60);      // Verde
  static const Color error = Color(0xFFE74C3C);        // Rojo
  static const Color warning = Color(0xFFF39C12);      // Naranja
  
  // Textos
  static const Color textPrimary = Color(0xFF2C3E50);  // Gris oscuro
  static const Color textSecondary = Color(0xFF7F8C8D); // Gris medio
  static const Color textLight = Color(0xFFBDC3C7);    // Gris claro
}

// =============================================================================
// CONFIGURACIÓN DE LA API
// =============================================================================

class ApiConfig {
  // URL base de la API (cambiar en producción)
     static const String baseUrl = 'http://192.168.1.5:8000';
  // static const String baseUrl = 'http://TU_IP:8000';  // Para dispositivo físico
  
  // Endpoints
  static const String login = '/login';
  static const String register = '/register';
  static const String userMe = '/users/me';
  static const String businesses = '/businesses';
  static const String businessesFeatured = '/businesses/featured';
  static const String myPoints = '/my-points';
  static const String myBusinesses = '/my-businesses';
}

// =============================================================================
// ESTILOS DE TEXTO
// =============================================================================

class AppTextStyles {
  static const TextStyle heading1 = TextStyle(
    fontSize: 28,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
  );
  
  static const TextStyle heading2 = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.bold,
    color: AppColors.textPrimary,
  );
  
  static const TextStyle heading3 = TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.w600,
    color: AppColors.textPrimary,
  );
  
  static const TextStyle body = TextStyle(
    fontSize: 16,
    color: AppColors.textPrimary,
  );
  
  static const TextStyle bodySmall = TextStyle(
    fontSize: 14,
    color: AppColors.textSecondary,
  );
  
  static const TextStyle button = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w600,
    color: AppColors.white,
  );
}

// =============================================================================
// CATEGORÍAS DE NEGOCIOS
// =============================================================================

class BusinessCategories {
  static const Map<String, String> names = {
    'bar': 'Bar',
    'restaurant': 'Restaurante',
    'cafe': 'Café',
    'hostel': 'Hostal',
    'hotel': 'Hotel',
    'tour_guide': 'Guía Turístico',
    'shop': 'Tienda',
    'art_gallery': 'Galería de Arte',
    'rental': 'Alquiler',
    'other': 'Otro',
  };
  
  static const Map<String, IconData> icons = {
    'bar': Icons.local_bar,
    'restaurant': Icons.restaurant,
    'cafe': Icons.coffee,
    'hostel': Icons.hotel,
    'hotel': Icons.business,
    'tour_guide': Icons.tour,
    'shop': Icons.store,
    'art_gallery': Icons.palette,
    'rental': Icons.directions_bike,
    'other': Icons.place,
  };
}   
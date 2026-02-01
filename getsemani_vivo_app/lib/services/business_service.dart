// lib/services/business_service.dart
// Servicio para conectar con los endpoints de negocios

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/business.dart';
import '../utils/constants.dart';

class BusinessService {
  
  // ==========================================================================
  // OBTENER NEGOCIOS APROBADOS
  // ==========================================================================
  
  static Future<List<Business>> getBusinesses({String? category}) async {
    try {
      String url = '${ApiConfig.baseUrl}${ApiConfig.businesses}';
      if (category != null) {
        url += '?category=$category';
      }

      final response = await http.get(Uri.parse(url));

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => Business.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  // ==========================================================================
  // OBTENER NEGOCIOS DESTACADOS
  // ==========================================================================
  
  static Future<List<Business>> getFeaturedBusinesses() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.businessesFeatured}'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => Business.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  // ==========================================================================
  // OBTENER DETALLE DE UN NEGOCIO
  // ==========================================================================
  
  static Future<Business?> getBusiness(int id) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.businesses}/$id'),
      );

      if (response.statusCode == 200) {
        return Business.fromJson(json.decode(response.body));
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  // ==========================================================================
  // OBTENER IMÁGENES DE UN NEGOCIO
  // ==========================================================================
  
  static Future<List<BusinessImage>> getBusinessImages(int businessId) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.businesses}/$businessId/images'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => BusinessImage.fromJson(json)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }
}
// lib/models/business.dart
// Modelo de Negocio

class Business {
  final int id;
  final String name;
  final String? description;
  final String category;
  final String? phone;
  final String? email;
  final String? website;
  final String? instagram;
  final String address;
  final double? latitude;
  final double? longitude;
  final String status;
  final bool isFeatured;
  final int pointsPer10000;
  final List<BusinessImage> images;

  Business({
    required this.id,
    required this.name,
    this.description,
    required this.category,
    this.phone,
    this.email,
    this.website,
    this.instagram,
    required this.address,
    this.latitude,
    this.longitude,
    required this.status,
    required this.isFeatured,
    required this.pointsPer10000,
    this.images = const [],
  });

  factory Business.fromJson(Map<String, dynamic> json) {
    return Business(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      category: json['category'],
      phone: json['phone'],
      email: json['email'],
      website: json['website'],
      instagram: json['instagram'],
      address: json['address'],
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
      status: json['status'],
      isFeatured: json['is_featured'] ?? false,
      pointsPer10000: json['points_per_10000'] ?? 1,
      images: json['images'] != null
          ? (json['images'] as List).map((i) => BusinessImage.fromJson(i)).toList()
          : [],
    );
  }

  // Obtener la imagen principal
  String? get primaryImageUrl {
    if (images.isEmpty) return null;
    final primary = images.where((img) => img.isPrimary).toList();
    if (primary.isNotEmpty) return primary.first.url;
    return images.first.url;
  }
}

class BusinessImage {
  final int id;
  final String filename;
  final String url;
  final bool isPrimary;
  final int order;

  BusinessImage({
    required this.id,
    required this.filename,
    required this.url,
    required this.isPrimary,
    required this.order,
  });

  factory BusinessImage.fromJson(Map<String, dynamic> json) {
    return BusinessImage(
      id: json['id'],
      filename: json['filename'],
      url: json['url'],
      isPrimary: json['is_primary'] ?? false,
      order: json['order'] ?? 0,
    );
  }
}
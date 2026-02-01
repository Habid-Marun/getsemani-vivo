// lib/models/user.dart
// Modelo de Usuario

class User {
  final int id;
  final String email;
  final String? fullName;
  final String? phone;
  final String role;
  final bool isActive;

  User({
    required this.id,
    required this.email,
    this.fullName,
    this.phone,
    required this.role,
    required this.isActive,
  });

  // Crear User desde JSON (respuesta de la API)
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      fullName: json['full_name'],
      phone: json['phone'],
      role: json['role'],
      isActive: json['is_active'] ?? true,
    );
  }

  // Convertir User a JSON (para enviar a la API)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'full_name': fullName,
      'phone': phone,
      'role': role,
      'is_active': isActive,
    };
  }
}
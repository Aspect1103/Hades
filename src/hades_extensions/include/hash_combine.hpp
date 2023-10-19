// Ensure this file is only included once
#pragma once

// ----- FUNCTIONS ------------------------------
/// Allows multiple hashes to be combined for a struct
///
/// @param seed - The seed for initialising the hasher.
/// @param v - The value to hash.
template <typename T>
inline void hash_combine(size_t &seed, const T &v) {
  std::hash<T> hasher;
  seed ^= hasher(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

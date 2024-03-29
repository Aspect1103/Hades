// Ensure this file is only included once
#pragma once

// Std headers
#include <memory>
#include <ranges>
#include <stdexcept>
#include <string>
#include <typeindex>

// Local headers
#include "steering.hpp"

// ----- TYPEDEFS ------------------------------
// Represents unique identifiers for game objects
using GameObjectID = int;
using ActionFunction = std::function<double(int)>;

// ----- CONSTANTS ------------------------------
// The percentage of velocity a game object will retain after a second.
constexpr double DAMPING = 0.0001;

// ----- BASE TYPES ------------------------------
// Add a forward declaration for the registry class
class Registry;

/// The base class for all components.
struct ComponentBase {
  /// The copy assignment operator.
  auto operator=(const ComponentBase &) -> ComponentBase & = default;

  /// The move assignment operator.
  auto operator=(ComponentBase &&) -> ComponentBase & = default;

  /// The default constructor.
  ComponentBase() = default;

  /// The virtual destructor.
  virtual ~ComponentBase() = default;

  /// The copy constructor.
  ComponentBase(const ComponentBase &) = default;

  /// The move constructor.
  ComponentBase(ComponentBase &&) = default;

  /// Checks if the component can have an indicator bar or not.
  ///
  /// @return Whether the component can have an indicator bar or not.
  [[nodiscard]] virtual auto has_indicator_bar() const -> bool { return false; }
};

/// The base class for all systems.
class SystemBase {
 public:
  /// The copy assignment operator.
  auto operator=(const SystemBase &) -> SystemBase & = default;

  /// The move assignment operator.
  auto operator=(SystemBase &&) -> SystemBase & = default;

  /// Initialise the object.
  ///
  /// @param registry - The registry that manages the game objects, components, and systems.
  explicit SystemBase(const Registry *registry) : registry(registry) {}

  /// The virtual destructor.
  virtual ~SystemBase() = default;

  /// The copy constructor.
  SystemBase(const SystemBase &) = default;

  /// The move constructor.
  SystemBase(SystemBase &&) = default;

  /// Get the registry that manages the game objects, components, and systems.
  ///
  /// @return The registry that manages the game objects, components, and systems.
  [[nodiscard]] auto get_registry() const -> const Registry * { return registry; }

  /// Process update logic for a system.
  virtual void update(double /*delta_time*/) const {}

 private:
  /// The registry that manages the game objects, components, and systems.
  const Registry *registry;
};

// ----- RAII TYPES ------------------------------
/// Allows for the RAII management of a Chipmunk2D object.
///
/// @tparam T - The type of Chipmunk2D object to manage.
/// @tparam Destructor - The destructor function for the Chipmunk2D object.
template <typename T, void (*Destructor)(T *)>
class ChipmunkHandle {
  /// The Chipmunk2D object.
  std::unique_ptr<T, void (*)(T *)> _obj;

 public:
  /// Initialise the object.
  ///
  /// @param obj - The Chipmunk2D object.
  explicit ChipmunkHandle(T *obj) : _obj(obj, Destructor) {}

  /// Destroy the object.
  ~ChipmunkHandle() = default;

  /// The copy constructor.
  ChipmunkHandle(const ChipmunkHandle &) = delete;

  /// The copy assignment operator.
  auto operator=(const ChipmunkHandle &) -> ChipmunkHandle & = delete;

  /// The move constructor.
  ChipmunkHandle(ChipmunkHandle &&) = delete;

  /// The move assignment operator.
  auto operator=(ChipmunkHandle &&) -> ChipmunkHandle & = delete;

  /// The dereference operator.
  auto operator*() const -> T * { return _obj.get(); }

  /// The arrow operator.
  auto operator->() const -> T * { return _obj.get(); }
};

// ----- EXCEPTIONS ------------------------------
/// Raised when an error occurs with the registry.
struct RegistryError final : std::runtime_error {
  /// Initialise the object
  ///
  /// @param error - The error message.
  explicit RegistryError(const std::string &error = "is not registered with the registry")
      : std::runtime_error("The templated type " + error + "."){};

  /// Initialise the object.
  ///
  /// @tparam T - The type of item that is not registered.
  /// @param not_registered_type - The type of item that is not registered.
  /// @param value - The value that is not registered.
  /// @param extra - Any extra information to add to the error message.
  template <typename T>
  RegistryError(const std::string &not_registered_type, const T &value, const std::string &extra = "")
      : std::runtime_error("The " + not_registered_type + " `" + std::to_string(value) +
                           "` is not registered with the registry" + extra + ".") {}
};

// ----- FUNCTIONS ------------------------------
/// Calculate the screen position based on a grid position.
///
/// @param position - The position in the grid.
/// @throws std::invalid_argument - If the position is negative.
/// @return The screen position of the grid position.
inline auto grid_pos_to_pixel(const cpVect &position) -> cpVect {
  if (position.x < 0 || position.y < 0) {
    throw std::invalid_argument("The position cannot be negative.");
  }
  return position * SPRITE_SIZE + SPRITE_SIZE / 2;
}

// ----- CLASSES ------------------------------
/// Manages game objects, components, and systems that are registered.
class Registry {
 public:
  /// Initialise the object.
  Registry() { cpSpaceSetDamping(*space_, DAMPING); }

  /// Create a new game object.
  ///
  /// @param position - The position of the game object.
  /// @param components - The components to add to the game object.
  /// @return The game object ID.
  auto create_game_object(const cpVect &position, const std::vector<std::shared_ptr<ComponentBase>> &&components)
      -> GameObjectID;

  /// Delete a game object.
  ///
  /// @param game_object_id - The game object ID.
  /// @throws RegistryError - If the game object is not registered.
  void delete_game_object(GameObjectID game_object_id);

  /// Checks if a game object has a given component or not.
  ///
  /// @param game_object_id - The game object ID.
  /// @param component_type - The type of component to check for.
  /// @return Whether the game object has the component or not.
  [[nodiscard]] auto has_component(const GameObjectID game_object_id, const std::type_index &component_type) const
      -> bool {
    return game_objects_.contains(game_object_id) && game_objects_.at(game_object_id).contains(component_type);
  }

  /// Get a component from the registry.
  ///
  /// @tparam T - The type of component to get.
  /// @param game_object_id - The game object ID.
  /// @throws RegistryError - If the game object is not registered or if the game object does not have the component.
  /// @return The component from the registry.
  template <typename T>
  auto get_component(const GameObjectID game_object_id) const -> std::shared_ptr<T> {
    return std::static_pointer_cast<T>(get_component(game_object_id, typeid(T)));
  }

  /// Get a component from the registry.
  ///
  /// @param game_object_id - The game object ID.
  /// @param component_type - The type of component to get.
  /// @throws RegistryError - If the game object is not registered or if the game object does not have the component.
  /// @return The component from the registry.
  [[nodiscard]] auto get_component(GameObjectID game_object_id, const std::type_index &component_type) const
      -> std::shared_ptr<ComponentBase>;

  /// Find all the game objects that have the required components.
  ///
  /// @tparam Ts - The types of components to find.
  /// @return The game objects that have the required components.
  template <typename... Ts>
  auto find_components() const {
    // Use ranges::filter to filter out the game objects that have all the components then use ranges::transform to get
    // only the game object ID and the required components
    return game_objects_ | std::views::filter([this](const auto &game_object) {
             const auto &[game_object_id, game_object_components] = game_object;
             return (has_component(game_object_id, typeid(Ts)) && ...);
           }) |
           std::views::transform([](const auto &game_object) {
             const auto &[game_object_id, game_object_components] = game_object;
             return std::make_tuple(
                 game_object_id,
                 std::make_tuple(std::static_pointer_cast<Ts>(game_object_components.at(typeid(Ts)))...));
           });
  }

  /// Add a system to the registry.
  ///
  /// @tparam T - The type of system to add.
  /// @throws RegistryError - If the system is already registered.
  template <typename T>
  void add_system() {
    // Check if the system is already registered
    const std::type_index system_type{typeid(T)};
    if (systems_.contains(system_type)) {
      throw RegistryError("is already registered with the registry");
    }

    // Add the system to the registry
    systems_[system_type] = std::make_shared<T>(this);
  }

  /// Get a system from the registry.
  ///
  /// @tparam T - The type of system to get.
  /// @throws RegistryError - If the system is not registered.
  /// @return The system from the registry.
  template <typename T>
  auto get_system() const -> std::shared_ptr<T> {
    // Check if the system is registered
    const std::type_index system_type{typeid(T)};
    const auto system_result{systems_.find(system_type)};
    if (system_result == systems_.end()) {
      throw RegistryError();
    }

    // Return the system
    return std::static_pointer_cast<T>(system_result->second);
  }

  /// Update all the systems in the registry.
  ///
  /// @param delta_time - The time interval since the last time the function was called.
  void update(const double delta_time) const {
    for (const auto &[_, system] : systems_) {
      system->update(delta_time);
    }
  }

  /// Get the Chipmunk2D space.
  ///
  /// @return The Chipmunk2D space.
  [[nodiscard]] auto get_space() const -> cpSpace * { return *space_; }

  /// Add a wall to the registry.
  ///
  /// @param wall - The wall to add to the registry.
  void add_wall(const cpVect &wall);

  /// Get the walls in the registry.
  ///
  /// @return The walls in the registry.
  [[nodiscard]] auto get_walls() const -> const std::unordered_set<cpVect> & { return walls_; }

 private:
  /// Add a Chipmunk2D object to the space.
  void add_chipmunk_object(cpBody *body, cpShape *shape, const cpVect &position) const;

  /// The next game object ID to use.
  GameObjectID next_game_object_id_{0};

  /// The game objects and their components registered with the registry.
  std::unordered_map<GameObjectID, std::unordered_map<std::type_index, std::shared_ptr<ComponentBase>>> game_objects_;

  /// The systems registered with the registry.
  std::unordered_map<std::type_index, std::shared_ptr<SystemBase>> systems_;

  /// The walls registered with the registry.
  std::unordered_set<cpVect> walls_;

  /// The Chipmunk2D space.
  ChipmunkHandle<cpSpace, cpSpaceFree> space_{cpSpaceNew()};
};

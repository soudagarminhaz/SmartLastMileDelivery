import streamlit as st

from app.models import (
    Delivery,
    Vehicle,
    Road,
    DeliveryProblem,
)

from app.services import DeliveryOptimizer


st.set_page_config(
    page_title="Smart Last-Mile Delivery",
    page_icon="🚚",
    layout="wide",
)


st.title(
    "🚚 Smart Last-Mile Delivery Optimization System"
)

st.write(
    """
    An intelligent delivery optimization system that
    automatically analyzes the problem and selects
    suitable algorithms.
    """
)


# ======================================================
# DELIVERY INPUT
# ======================================================

st.header("📦 Delivery Information")

delivery_count = st.number_input(
    "Number of deliveries",
    min_value=1,
    max_value=20,
    value=5,
    step=1,
)


deliveries: list[Delivery] = []


for index in range(delivery_count):

    st.subheader(
        f"Delivery {index + 1}"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        delivery_id = st.text_input(
            "ID",
            value=f"D{index + 1:03d}",
            key=f"delivery_id_{index}",
        )

    with col2:
        destination = st.text_input(
            "Destination",
            value=chr(65 + index),
            key=f"destination_{index}",
        )

    with col3:
        weight = st.number_input(
            "Weight (kg)",
            min_value=0.1,
            value=2.0,
            step=0.5,
            key=f"weight_{index}",
        )

    with col4:
        priority = st.number_input(
            "Priority",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
            key=f"priority_{index}",
        )

    with col5:
        deadline = st.number_input(
            "Deadline",
            min_value=1,
            value=60,
            step=5,
            key=f"deadline_{index}",
        )

    deliveries.append(
        Delivery(
            delivery_id=delivery_id,
            destination=destination,
            weight=weight,
            priority=priority,
            deadline=deadline,
        )
    )


# ======================================================
# VEHICLE INPUT
# ======================================================

st.header("🚚 Vehicle Information")

vehicle_count = st.number_input(
    "Number of vehicles",
    min_value=1,
    max_value=10,
    value=2,
    step=1,
)


vehicles: list[Vehicle] = []


for index in range(vehicle_count):

    st.subheader(
        f"Vehicle {index + 1}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        vehicle_id = st.text_input(
            "Vehicle ID",
            value=f"V{index + 1:03d}",
            key=f"vehicle_id_{index}",
        )

    with col2:
        capacity = st.number_input(
            "Capacity (kg)",
            min_value=1.0,
            value=15.0,
            step=1.0,
            key=f"capacity_{index}",
        )

    with col3:
        vehicle_type = st.selectbox(
            "Vehicle Type",
            [
                "Van",
                "Electric",
                "Truck",
            ],
            key=f"vehicle_type_{index}",
        )

    vehicles.append(
        Vehicle(
            vehicle_id=vehicle_id,
            capacity=capacity,
            start_location="DEPOT",
            vehicle_type=vehicle_type,
        )
    )


# ======================================================
# ROAD NETWORK
# ======================================================

st.header("🛣️ Road Network")

road_count = st.number_input(
    "Number of roads",
    min_value=1,
    max_value=50,
    value=8,
    step=1,
)


roads: list[Road] = []


for index in range(road_count):

    col1, col2, col3 = st.columns(3)

    with col1:
        source = st.text_input(
            "Source",
            value="DEPOT",
            key=f"road_source_{index}",
        )

    with col2:
        destination = st.text_input(
            "Destination",
            value="A",
            key=f"road_destination_{index}",
        )

    with col3:
        distance = st.number_input(
            "Distance (km)",
            min_value=0.1,
            value=5.0,
            step=0.5,
            key=f"road_distance_{index}",
        )

    roads.append(
        Road(
            source=source,
            destination=destination,
            distance=distance,
        )
    )


# ======================================================
# OPTIMIZATION
# ======================================================

st.divider()

if st.button(
    "🚀 Optimize Delivery Plan",
    type="primary",
):

    problem = DeliveryProblem(
        deliveries=deliveries,
        vehicles=vehicles,
        roads=roads,
    )

    try:

        optimizer = DeliveryOptimizer()

        result = optimizer.optimize(
            problem
        )

        st.success(
            "Optimization completed successfully!"
        )

        # ------------------------------------------------
        # ALGORITHM SELECTION
        # ------------------------------------------------

        st.header(
            "🧠 Automatic Algorithm Selection"
        )

        for algorithm in (
            result.selected_algorithms
        ):

            st.write(
                f"✅ {algorithm}"
            )

        # ------------------------------------------------
        # PRIORITIZED DELIVERIES
        # ------------------------------------------------

        st.header(
            "📊 Prioritized Deliveries"
        )

        for delivery in (
            result.prioritized_deliveries
        ):

            st.write(
                f"**{delivery.delivery_id}** → "
                f"{delivery.destination} | "
                f"Priority: {delivery.priority} | "
                f"Weight: {delivery.weight} kg"
            )

        # ------------------------------------------------
        # VEHICLE ASSIGNMENT
        # ------------------------------------------------

        st.header(
            "🚚 Vehicle Assignments"
        )

        for vehicle_id, assigned in (
            result.assignments.items()
        ):

            st.subheader(
                vehicle_id
            )

            if not assigned:

                st.write(
                    "No deliveries assigned."
                )

            for delivery in assigned:

                st.write(
                    f"📦 {delivery.delivery_id} → "
                    f"{delivery.destination}"
                )

        # ------------------------------------------------
        # SHORTEST PATHS
        # ------------------------------------------------

        st.header(
            "🗺️ Shortest Paths"
        )

        for delivery_id, path in (
            result.shortest_paths.items()
        ):

            st.write(
                f"**{delivery_id}**"
            )

            st.code(
                str(path)
            )

        # ------------------------------------------------
        # DP RESULT
        # ------------------------------------------------

        st.header(
            "🎯 Capacity Optimization"
        )

        for delivery in (
            result.capacity_selection
        ):

            st.write(
                f"📦 {delivery.delivery_id} → "
                f"{delivery.destination}"
            )

        # ------------------------------------------------
        # ADVANCED ROUTES
        # ------------------------------------------------

        if result.backtracking_route:

            st.header(
                "🔄 Backtracking Route"
            )

            st.write(
                " → ".join(
                    delivery.destination
                    for delivery
                    in result.backtracking_route
                )
            )

        if result.branch_bound_route:

            st.header(
                "🌳 Branch & Bound Route"
            )

            st.write(
                " → ".join(
                    delivery.destination
                    for delivery
                    in result.branch_bound_route
                )
            )

        # ------------------------------------------------
        # SYSTEM MESSAGES
        # ------------------------------------------------

        st.header(
            "ℹ️ Optimization Details"
        )

        for message in result.messages:

            st.write(
                f"• {message}"
            )

    except Exception as error:

        st.error(
            f"Optimization failed: {error}"
        )
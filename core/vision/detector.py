def detect(self, image: np.ndarray) -> Dict:

    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Invalid image provided to detector.")

    if self.model is None:
        return self._synthetic_detection(image)

    try:
        start = time.time()
        results = self.model(image, verbose=False)[0]
        inference_time = (time.time() - start) * 1000

        if results.boxes is None:
            print("[YOLO] No detections at all.")
            return self._empty_detection(inference_time)

        elements = []
        class_counts = {}
        confidences = []

        raw_count = len(results.boxes)

        for box in results.boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            label = self.model.names.get(cls_id, "unknown")
            label = str(label).lower().strip().replace(" ", "_")

            if label == "dimension":
                continue

            if label not in self.allowed_classes:
                continue

            if conf < self.conf_threshold:
                continue

            class_counts[label] = class_counts.get(label, 0) + 1
            confidences.append(conf)

            elements.append({
                "id": f"{label}_{len(elements)+1}",
                "type": label,
                "confidence": round(conf, 4),
                "bbox": [
                    int(max(0, x1)),
                    int(max(0, y1)),
                    int(max(0, x2)),
                    int(max(0, y2))
                ],
                "synthetic": False
            })

        print(f"[YOLO] Raw detections: {raw_count}")
        print(f"[YOLO] After filtering: {len(elements)}")

        if not elements:
            return self._empty_detection(inference_time)

        avg_conf = sum(confidences) / len(confidences)

        return {
            "elements": elements,
            "class_counts": class_counts,
            "total_detections": len(elements),
            "model_used": self.model_used,
            "inference_time_ms": round(inference_time, 2),
            "average_confidence": round(avg_conf, 4)
        }

    except Exception as e:
        print(f"[YOLO] Detection failed: {e}")
        return self._synthetic_detection(image)
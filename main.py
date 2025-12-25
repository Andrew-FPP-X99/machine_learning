import sys
import config
from src import data_loader, clustering, evaluator, geo_processor, visualizer

def main():
    print("="*40 + "\n   DISASTER RISK ANALYTICS PIPELINE\n" + "="*40)
    
    try:
        # 1. Ingestion
        df_raw, gdf_raw = data_loader.load_data(config.FILE_CSV, config.FILE_GEOJSON)

        # 2. Machine Learning
        df_clustered, X_scaled = clustering.run_kmeans(
            df_raw, config.FEATURES, config.N_CLUSTERS
        )

        # 3. Evaluation
        evaluator.calculate_metrics(X_scaled, df_clustered['cluster_label'])
        evaluator.print_insights(df_clustered, 'cluster_label', config.FEATURES)

        # 4. Spatial Processing
        gdf_final = geo_processor.process_spatial_join(
            gdf_raw, df_clustered, config.TARGET_PROV, config.COL_CITY
        )

        # 5. Visualization
        visualizer.plot_map(gdf_final, config.IMG_MAP, 'cluster_label', config.TARGET_PROV)
        
        visualizer.plot_pca(
            X_scaled, 
            df_clustered['cluster_label'], 
            config.IMG_PCA,
            df_original=df_clustered 
        )

        print("\n Pipeline Finished Successfully.")

    except Exception as e:
        print(f"\n FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
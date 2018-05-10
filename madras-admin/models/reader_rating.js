'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_rating', {
  }, {
    tableName: 'reader_rating',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_application, {
      foreignKey: 'application_id',
      
      as: '_application_id',
    });
    
  };

  return Model;
};

